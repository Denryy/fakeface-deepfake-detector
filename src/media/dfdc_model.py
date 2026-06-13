"""
dfdc_model.py — DeepFakeClassifier (DFDC-winner, selimsef) нашим кодом для inference.

Архитектура воспроизведена вручную (НЕ исполняем чужой код): timm EfficientNet-B7
(`forward_features`) -> global average pool -> Linear(2560, 1). Веса selimsef
(`final_*_DeepFakeClassifier_tf_efficientnet_b7_ns_*`) грузятся безопасно
(`weights_only=True`). Файлы весов локальные (vendor/, в репозиторий не входят).

Обучен на DFDC -> заточен на FACE-SWAP дипфейки (в отличие от NPR, который про
полностью сгенерированные изображения). Препроцессинг: кроп лица (с margin) ->
380x380 -> ImageNet-нормализация.
"""

from __future__ import annotations

import torch
import torch.nn as nn

ENCODER = "tf_efficientnet_b7.ns_jft_in1k"
FEATURES = 2560
INPUT = 380

_cache: dict = {}  # weights_path -> (model, device, load_report)


class DFDCNet(nn.Module):
    """EfficientNet-B7 (timm) энкодер + бинарная голова (как selimsef DeepFakeClassifier)."""

    def __init__(self):
        super().__init__()
        import timm
        self.encoder = timm.create_model(ENCODER, pretrained=False, num_classes=0, global_pool="")
        self.fc = nn.Linear(FEATURES, 1)

    def forward(self, x):
        x = self.encoder.forward_features(x)   # [B, 2560, H, W]
        x = x.mean(dim=[2, 3])                  # global average pool -> [B, 2560]
        return self.fc(x)                       # [B, 1] логит


def load_dfdc(weights_path: str, device: str = "cpu"):
    """Создать DFDCNet и загрузить ТОЛЬКО веса (weights_only=True). Кэш по пути."""
    if weights_path in _cache:
        return _cache[weights_path]
    model = DFDCNet()
    # checkpoint содержит numpy-метаданные (epoch и т.п.) как numpy scalar/dtype —
    # это БЕЗОПАСНЫЕ типы данных (не код). Разрешаем их с ЯВНЫМ именем (numpy 2.x
    # переименовал модуль), оставив weights_only=True (защита от исполнения кода).
    import numpy as _np
    _sc = None
    try:
        _sc = _np.core.multiarray.scalar
    except Exception:  # noqa: BLE001
        try:
            _sc = _np._core.multiarray.scalar
        except Exception:  # noqa: BLE001
            pass
    adds = []
    if _sc is not None:
        adds.append((_sc, "numpy.core.multiarray.scalar"))
    adds.append((_np.dtype, "numpy.dtype"))
    for nm in ("Float64DType", "Int64DType", "Float32DType"):
        if hasattr(_np.dtypes, nm):
            adds.append((getattr(_np.dtypes, nm), f"numpy.dtypes.{nm}"))
    try:
        torch.serialization.add_safe_globals(adds)
    except Exception:  # noqa: BLE001 — старый torch без tuple-формы
        torch.serialization.add_safe_globals([a[0] for a in adds])
    state = torch.load(weights_path, map_location="cpu", weights_only=True)
    if isinstance(state, dict):
        state = state.get("state_dict", state)
    state = {k.replace("module.", "", 1): v for k, v in state.items()}
    report = model.load_state_dict(state, strict=False)
    model.to(device).eval()
    _cache[weights_path] = (model, device, report)
    return _cache[weights_path]


def _tf():
    from torchvision import transforms
    return transforms.Compose([
        transforms.Resize((INPUT, INPUT)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


def dfdc_fake_probs(pil_images: list, weights_path: str, device: str = "cpu") -> list:
    """Вероятности 'fake' для одной модели (по списку кропов лиц)."""
    tf = _tf()
    model, dev, _ = load_dfdc(weights_path, device)
    batch = torch.stack([tf(im.convert("RGB")) for im in pil_images]).to(dev)
    with torch.no_grad():
        probs = torch.sigmoid(model(batch).squeeze(-1))
    vals = probs.tolist()
    return [float(v) for v in (vals if isinstance(vals, list) else [vals])]


def dfdc_fake_probs_ensemble(pil_images: list, weights_paths: list, device: str = "cpu") -> tuple:
    """Среднее по нескольким B7. Возвращает (per_image_avg, per_model_overall_avg)."""
    if not weights_paths:
        return [], {}
    per_model = {}        # path -> список вероятностей по изображениям
    for wp in weights_paths:
        try:
            per_model[wp] = dfdc_fake_probs(pil_images, wp, device)
        except Exception:  # noqa: BLE001 — сбойная модель пропускается
            continue
    if not per_model:
        return [], {}
    n = len(pil_images)
    avg = [sum(per_model[wp][i] for wp in per_model) / len(per_model) for i in range(n)]
    overall = {wp.split("/")[-1].split("\\")[-1]: round(sum(v) / len(v), 3) for wp, v in per_model.items()}
    return avg, overall
