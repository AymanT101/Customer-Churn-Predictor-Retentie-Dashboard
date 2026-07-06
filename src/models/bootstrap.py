"""Ensure model artifacts exist before serving predictions."""

from __future__ import annotations

from src.config import MODEL_PATH
from src.models.predict import load_artifact
from src.models.train import train_model


def ensure_model_artifacts() -> None:
    """Generate data and train the model when artifacts are missing."""
    if not MODEL_PATH.exists():
        train_model()
    load_artifact.cache_clear()
    load_artifact()
