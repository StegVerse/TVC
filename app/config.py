from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class ProviderConfig:
    """Canonical description of a single AI provider/model combo."""

    name: str               # e.g. "github_models" or "openai"
    model: str              # e.g. "openai/gpt-4.1-mini"
    endpoint: str | None    # optional explicit base URL
    notes: str | None = None


@dataclass
class StegTVCSettings:
    """Top-level settings for StegTVC Core."""

    service_name: str = "StegTVC"
    version: str = os.getenv("STEGTVC_VERSION", "0.1.0")

    # Where StegTVC itself is reachable (for self-reports)
    public_url: str | None = os.getenv("STEGTVC_PUBLIC_URL")

    # Default provider/model for generic text tasks
    default_provider_name: str = os.getenv("STEGTVC_DEFAULT_PROVIDER", "github_models")
    default_model: str = os.getenv("STEGTVC_DEFAULT_MODEL", "openai/gpt-4.1-mini")

    # Optional explicit endpoints (most callers can ignore these)
    github_models_endpoint: str = os.getenv(
        "STEGTVC_GITHUB_MODELS_ENDPOINT",
        "https://models.github.ai/inference/chat/completions",
    )
    openai_endpoint: str = os.getenv(
        "STEGTVC_OPENAI_ENDPOINT",
        "https://api.openai.com/v1/chat/completions",
    )


@lru_cache(maxsize=1)
def get_settings() -> StegTVCSettings:
    """Cached settings instance."""
    return StegTVCSettings()


def get_default_provider() -> ProviderConfig:
    """Return a ProviderConfig instance for the default provider/model."""
    settings = get_settings()

    if settings.default_provider_name.lower() in {"github_models", "github"}:
        endpoint = settings.github_models_endpoint
        name = "github_models"
    elif settings.default_provider_name.lower() in {"openai"}:
        endpoint = settings.openai_endpoint
        name = "openai"
    else:
        # Fallback – treat as opaque provider name
        endpoint = None
        name = settings.default_provider_name

    return ProviderConfig(
        name=name,
        model=settings.default_model,
        endpoint=endpoint,
        notes="Default provider selected by StegTVC. Safe for generic text tasks.",
    )