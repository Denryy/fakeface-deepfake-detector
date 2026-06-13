"""
npr_model.py — архитектура NPR-детектора, переписанная НАШИМ кодом для inference.

Воспроизведена вручную по описанию NPR (CVPR 2024, "Rethinking the Up-Sampling
Operations…", chuangchuangtan/NPR-DeepfakeDetection), чтобы НЕ исполнять чужой
код. Мы грузим только веса через `weights_only=True` (тензоры, без pickle-кода).
Файл весов `NPR.pth` — внешний/локальный, путь задаётся при загрузке (в репозиторий
не коммитится).

NPR = усечённый ResNet (Bottleneck, layer1+layer2) поверх фичи Neighboring Pixel
Relationships: NPR(x) = x − upsample(downsample(x)). Выход — 1 логит;
sigmoid → вероятность 'fake'. Хорошо обобщается на сгенерированные изображения
(GAN/diffusion/Midjourney), хуже — на face-swap.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def _conv3x3(i, o, s=1):
    return nn.Conv2d(i, o, 3, stride=s, padding=1, bias=False)


def _conv1x1(i, o, s=1):
    return nn.Conv2d(i, o, 1, stride=s, bias=False)


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super().__init__()
        self.conv1 = _conv1x1(inplanes, planes)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = _conv3x3(planes, planes, stride)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = _conv1x1(planes, planes * self.expansion)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        idt = x
        o = self.relu(self.bn1(self.conv1(x)))
        o = self.relu(self.bn2(self.conv2(o)))
        o = self.bn3(self.conv3(o))
        if self.downsample is not None:
            idt = self.downsample(x)
        return self.relu(o + idt)


class NPRNet(nn.Module):
    """Усечённый ResNet50 (только layer1+layer2) с NPR-фичей на входе."""

    def __init__(self, layers=(3, 4), num_classes: int = 1):
        super().__init__()
        self.inplanes = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(64, layers[0])
        self.layer2 = self._make_layer(128, layers[1], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(512, num_classes)

    def _make_layer(self, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * Bottleneck.expansion:
            downsample = nn.Sequential(
                _conv1x1(self.inplanes, planes * Bottleneck.expansion, stride),
                nn.BatchNorm2d(planes * Bottleneck.expansion),
            )
        layers = [Bottleneck(self.inplanes, planes, stride, downsample)]
        self.inplanes = planes * Bottleneck.expansion
        for _ in range(1, blocks):
            layers.append(Bottleneck(self.inplanes, planes))
        return nn.Sequential(*layers)

    def _interp(self, img, factor):
        return F.interpolate(
            F.interpolate(img, scale_factor=factor, mode="nearest", recompute_scale_factor=True),
            scale_factor=1 / factor, mode="nearest", recompute_scale_factor=True,
        )

    def forward(self, x):
        npr = x - self._interp(x, 0.5)
        x = self.relu(self.bn1(self.conv1(npr * 2.0 / 3.0)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.avgpool(x).flatten(1)
        return self.fc1(x)


_cache = None  # (model, device)


def load_npr(weights_path: str, device: str = "cpu"):
    """Создать NPRNet и загрузить ТОЛЬКО веса (weights_only=True — без исполнения кода)."""
    global _cache
    if _cache is not None:
        return _cache
    model = NPRNet()
    state = torch.load(weights_path, map_location="cpu", weights_only=True)
    if isinstance(state, dict) and "model" in state and isinstance(state["model"], dict):
        state = state["model"]
    # снять возможный префикс "module."
    state = {k.replace("module.", "", 1): v for k, v in state.items()}
    try:
        model.load_state_dict(state, strict=True)
    except Exception:  # noqa: BLE001 — допускаем небольшие расхождения ключей
        model.load_state_dict(state, strict=False)
    model.to(device).eval()
    _cache = (model, device)
    return _cache


def npr_fake_probs(pil_images: list, weights_path: str, device: str = "cpu") -> list:
    """Вернуть вероятности 'fake' (sigmoid) для списка PIL-изображений."""
    from torchvision import transforms

    tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    model, dev = load_npr(weights_path, device)
    batch = torch.stack([tf(im.convert("RGB")) for im in pil_images]).to(dev)
    with torch.no_grad():
        probs = torch.sigmoid(model(batch).squeeze(-1))
    vals = probs.tolist()
    return [float(v) for v in (vals if isinstance(vals, list) else [vals])]
