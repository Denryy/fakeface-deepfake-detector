"""
fakeface_detector_real.py — РЕАЛЬНЫЙ детектор deepfake по видео (Студент 6).

В отличие от `fakeface_detector_stub.py` (эвристика по метке/тексту), этот модуль
реально анализирует видео И аудио:
  - has_face                  — детекция лица в кадрах (OpenCV Haar cascade);
  - possible_deepfake         — предобученная HF ViT-модель по кропам лиц;
  - synthetic_voice_suspected — извлечение аудио (ffmpeg) + HF audio-anti-spoofing
                                модель (Wav2Vec2) по дорожке голоса;
  - lip_sync_anomaly          — НЕ анализируется (нужен SyncNet), возвращается False.

Контракт выхода (`media_anomalies`, 4 поля) совместим со схемой §5 и со stub,
поэтому downstream (Студент 7 risk_engine, Студент 8 граф) ничего не меняет.

Запуск:
    python src/media/fakeface_detector_real.py --video path/to/video.mp4
    (--no-audio чтобы отключить аудио-ветку)

Откат: если зависимости/модель недоступны — фолбэк на stub.analyze_media().
Это НЕ production-детектор: точность ограничена готовыми моделями (см. findings §8).
"""

from __future__ import annotations

import argparse
import json
from typing import Optional

# Ансамбль готовых deepfake-моделей (HuggingFace, ViT). У каждой свой режим:
#   crop  — классифицирует кроп лица (модель обучена на лицах);
#   frame — классифицирует целый кадр (модель обучена на полных изображениях).
# Итог = МАКСИМУМ по моделям ("если хоть одна заподозрила") -> выше recall,
# чтобы реже пропускать дипфейки. Цена — выше шанс ложного срабатывания.
FACE_MODELS = [
    {"id": "prithivMLmods/Deep-Fake-Detector-Model", "mode": "crop"},
    {"id": "dima806/deepfake_vs_real_image_detection", "mode": "frame"},
    {"id": "Wvolf/ViT_Deepfake_Detection", "mode": "frame"},
]
DEEPFAKE_MODEL = FACE_MODELS[0]["id"]  # для совместимости/логов
# Готовая audio-anti-spoofing модель (Wav2Vec2). Выбрана по тесту: реальный
# голос -> P(fake)=0.0, синтетический (gTTS/SAPI) -> P(fake)=1.0.
AUDIO_MODEL = "motheecreator/Deepfake-audio-detection"
DEFAULT_MAX_FRAMES = 16
DEEPFAKE_THRESHOLD = 0.5
VOICE_THRESHOLD = 0.5
AUDIO_SR = 16000
AUDIO_MAX_SECONDS = 20
MIN_FACE = (60, 60)

_face_cache: dict = {}  # id -> (model, processor, device)
_device = None          # "cuda" / "cpu"
_cascade = None         # ленивый каскад лиц
_vmodel = None          # ленивая audio-модель
_vfe = None             # ленивый audio feature extractor
_vdevice = None         # "cuda" / "cpu" (audio)


def _load_face_model(model_id: str):
    """Лениво загрузить (и закэшировать) одну HF-модель + image processor на GPU."""
    global _device
    if model_id in _face_cache:
        return _face_cache[model_id]
    import torch
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    proc = AutoImageProcessor.from_pretrained(model_id, use_fast=False)
    model = AutoModelForImageClassification.from_pretrained(model_id)
    _device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(_device).eval()
    _face_cache[model_id] = (model, proc, _device)
    return _face_cache[model_id]


def _face_cascade():
    """Ленивая инициализация Haar-каскада лиц из поставки OpenCV."""
    global _cascade
    if _cascade is None:
        import cv2
        _cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    return _cascade


def extract_frames(video_path: str, max_frames: int = DEFAULT_MAX_FRAMES) -> list:
    """Равномерно сэмплировать до `max_frames` кадров (BGR) из видео."""
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"не удалось открыть видео: {video_path}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    frames = []
    if total <= 0:
        while len(frames) < max_frames:
            ok, fr = cap.read()
            if not ok:
                break
            frames.append(fr)
    else:
        step = max(1, total // max_frames)
        for idx in range(0, total, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ok, fr = cap.read()
            if ok:
                frames.append(fr)
            if len(frames) >= max_frames:
                break
    cap.release()
    return frames


def detect_face_crops(frame_bgr) -> list:
    """Вернуть PIL-изображения (RGB) найденных в кадре лиц."""
    import cv2
    from PIL import Image
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade().detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=MIN_FACE)
    crops = []
    for (x, y, w, h) in faces:
        rgb = cv2.cvtColor(frame_bgr[y:y + h, x:x + w], cv2.COLOR_BGR2RGB)
        crops.append(Image.fromarray(rgb))
    return crops


def _classify_with(model_id: str, images: list) -> list:
    """Прогнать PIL-изображения через указанную модель -> список вероятностей 'fake'."""
    import torch
    model, proc, device = _load_face_model(model_id)
    inputs = proc(images=images, return_tensors="pt").to(device)
    with torch.no_grad():
        probs = torch.softmax(model(**inputs).logits, dim=-1)
    labels = {int(k): str(v).lower() for k, v in model.config.id2label.items()}
    n = probs.shape[-1]
    names = [labels.get(i, "") for i in range(n)]
    fake_idx = next((i for i, nm in enumerate(names) if "fake" in nm), None)
    real_idx = next((i for i, nm in enumerate(names) if "real" in nm), None)
    out = []
    for row in probs.tolist():
        if fake_idx is not None:
            out.append(float(row[fake_idx]))
        elif real_idx is not None:
            out.append(1.0 - float(row[real_idx]))
        else:
            out.append(0.0)
    return out


def _load_voice_classifier():
    """Лениво загрузить (один раз) HF audio-anti-spoofing модель на GPU при наличии."""
    global _vmodel, _vfe, _vdevice
    if _vmodel is not None:
        return _vmodel, _vfe, _vdevice
    import torch
    from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
    _vfe = AutoFeatureExtractor.from_pretrained(AUDIO_MODEL)
    _vmodel = AutoModelForAudioClassification.from_pretrained(AUDIO_MODEL)
    _vdevice = "cuda" if torch.cuda.is_available() else "cpu"
    _vmodel.to(_vdevice).eval()
    return _vmodel, _vfe, _vdevice


def extract_audio(video_path: str, sr: int = AUDIO_SR, max_seconds: int = AUDIO_MAX_SECONDS):
    """Извлечь моно-аудио (numpy float32, `sr` Гц) из видео через ffmpeg.

    Возвращает waveform или None, если в видео нет аудиодорожки.
    """
    import os
    import tempfile
    import subprocess
    import imageio_ffmpeg
    import soundfile as sf

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out = os.path.join(tempfile.gettempdir(), "ffd_audio16k.wav")
    cmd = [ff, "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", str(sr),
           "-t", str(max_seconds), "-f", "wav", out]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0 or not os.path.exists(out):
        return None
    audio, _ = sf.read(out, dtype="float32")
    return audio if audio.size > 0 else None


def classify_voice(waveform) -> float:
    """Вернуть вероятность класса 'fake/spoof' для голосовой дорожки."""
    import torch
    model, fe, device = _load_voice_classifier()
    inputs = fe(waveform, sampling_rate=AUDIO_SR, return_tensors="pt").to(device)
    with torch.no_grad():
        probs = torch.softmax(model(**inputs).logits, dim=-1)[0].tolist()
    labels = {int(k): str(v).lower() for k, v in model.config.id2label.items()}
    fake_idx = next(
        (i for i in range(len(labels)) if any(w in labels[i] for w in ("fake", "spoof", "synthetic"))),
        None,
    )
    return float(probs[fake_idx]) if fake_idx is not None else 0.0


def _analyze_voice(video_path: str, voice_threshold: float) -> tuple[bool, Optional[float], bool]:
    """Аудио-ветка: вернуть (synthetic_voice, voice_fake_prob, has_audio)."""
    try:
        wav = extract_audio(video_path)
    except Exception:  # noqa: BLE001 — аудио опционально, не должно ронять видео-часть
        return False, None, False
    if wav is None or len(wav) < AUDIO_SR // 10:  # < 0.1 c
        return False, None, False
    p = classify_voice(wav)
    return p >= voice_threshold, round(p, 3), True


def analyze_video(
    video_path: str,
    max_frames: int = DEFAULT_MAX_FRAMES,
    threshold: float = DEEPFAKE_THRESHOLD,
    analyze_audio: bool = True,
    voice_threshold: float = VOICE_THRESHOLD,
) -> tuple[dict, dict]:
    """Проанализировать видео и вернуть (media_anomalies, details).

    Реально анализируются `has_face`, `possible_deepfake` (видео) и
    `synthetic_voice_suspected` (аудио, если `analyze_audio`). `lip_sync_anomaly`
    не анализируется (нужен SyncNet) и всегда False.
    """
    import cv2
    from PIL import Image

    frames = extract_frames(video_path, max_frames)
    if not frames:
        raise RuntimeError("не извлечено ни одного кадра")

    face_imgs, frames_with_face = [], 0
    for fr in frames:
        crops = detect_face_crops(fr)
        if crops:
            frames_with_face += 1
            face_imgs.append(crops[0])
    whole_imgs = [Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)) for fr in frames]
    has_face = frames_with_face > 0

    # Ансамбль: каждая модель в своём режиме (crop -> лица, frame -> целые кадры),
    # итог = МАКСИМУМ по моделям (если хоть одна заподозрила) -> выше recall.
    per_model = {}
    for m in FACE_MODELS:
        imgs = face_imgs if m["mode"] == "crop" else whole_imgs
        if not imgs:
            continue
        try:
            probs = _classify_with(m["id"], imgs)
            per_model[m["id"]] = round(sum(probs) / len(probs), 3)
        except Exception:  # noqa: BLE001 — одна сбойная модель не должна валить остальные
            continue
    avg = max(per_model.values()) if per_model else 0.0
    possible = avg >= threshold
    note = "ok" if per_model else "no_face/model: оценка по лицу пропущена"

    synthetic_voice, voice_p, has_audio = (
        _analyze_voice(video_path, voice_threshold) if analyze_audio else (False, None, False)
    )

    anomalies = {
        "has_face": bool(has_face),
        "possible_deepfake": bool(possible),
        "synthetic_voice_suspected": bool(synthetic_voice),
        "lip_sync_anomaly": False,
    }
    details = {
        "frames_analyzed": len(frames),
        "frames_with_face": frames_with_face,
        "faces_classified": len(face_imgs),
        "avg_fake_probability": round(avg, 3),   # ансамбль = максимум по моделям
        "face_models": per_model,                 # разбивка вероятностей по моделям
        "ensemble": "max",
        "threshold": threshold,
        "has_audio": has_audio,
        "voice_fake_probability": voice_p,
        "voice_threshold": voice_threshold,
        "audio_model": AUDIO_MODEL if analyze_audio else None,
        "note": note,
    }
    return anomalies, details


def analyze_video_safe(video_path: str, **kwargs) -> tuple[dict, dict]:
    """Как analyze_video, но с откатом на stub при любой ошибке (deps/model/IO)."""
    try:
        return analyze_video(video_path, **kwargs)
    except Exception as e:  # noqa: BLE001 — фолбэк должен ловить всё
        try:
            from fakeface_detector_stub import analyze_media
        except ImportError:
            from src.media.fakeface_detector_stub import analyze_media
        return analyze_media(), {"fallback": True, "error": f"{type(e).__name__}: {e}"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Real video deepfake detector (Student 6)")
    ap.add_argument("--video", required=True, help="путь к видеофайлу (.mp4 и т.п.)")
    ap.add_argument("--max-frames", type=int, default=DEFAULT_MAX_FRAMES)
    ap.add_argument("--threshold", type=float, default=DEEPFAKE_THRESHOLD)
    ap.add_argument("--voice-threshold", type=float, default=VOICE_THRESHOLD)
    ap.add_argument("--no-audio", action="store_true", help="отключить аудио-ветку")
    args = ap.parse_args()

    anomalies, details = analyze_video_safe(
        args.video, max_frames=args.max_frames, threshold=args.threshold,
        analyze_audio=not args.no_audio, voice_threshold=args.voice_threshold,
    )
    print(json.dumps({"media_anomalies": anomalies, "details": details}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
