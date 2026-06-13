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

_cache = None  # (model, device, load_report)


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
    """Создать DFDCNet и загрузить ТОЛЬКО веса (weights_only=True)."""
    global _cache
    if _cache is not None:
        return _cache
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
    _cache = (model, device, report)
    return _cache


def dfdc_fake_probs(pil_images: list, weights_path: str, device: str = "cpu") -> list:
    """Вернуть вероятности 'fake' (sigmoid) для списка PIL-изображений (кропы лиц)."""
    from torchvision import transforms

    tf = transforms.Compose([
        transforms.Resize((INPUT, INPUT)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    model, dev, _ = load_dfdc(weights_path, device)
    batch = torch.stack([tf(im.convert("RGB")) for im in pil_images]).to(dev)
    with torch.no_grad():
        probs = torch.sigmoid(model(batch).squeeze(-1))
    vals = probs.tolist()
    return [float(v) for v in (vals if isinstance(vals, list) else [vals])]
