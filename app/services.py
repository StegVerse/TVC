from __future__ import annotations

from typing import Dict, Any

from .config import get_default_provider
from .models import ProviderResolveRequest, ProviderResolveResponse, ProviderInfo


def resolve_provider(payload: ProviderResolveRequest) -> ProviderResolveResponse:
    """
    Very first version of the routing logic.

    For now:
    - Always returns the global default provider/model.
    - Uses 'importance' to set some suggested parameters (for the caller to respect).
    """

    base = get_default_provider()

    provider = ProviderInfo(
        name=base.name,
        model=base.model,
        endpoint=base.endpoint,
        notes=base.notes,
    )

    # Simple constraint hints based on importance
    constraints: Dict[str, Any] = {
        "max_tokens": 900,
        "temperature": 0.2,
    }

    if payload.importance == "low":
        constraints["max_tokens"] = 600
        constraints["temperature"] = 0.3
    elif payload.importance in {"high", "critical"}:
        constraints["max_tokens"] = 1800
        constraints["temperature"] = 0.15

    return ProviderResolveResponse(
        provider=provider,
        use_case=payload.use_case,
        constraints=constraints,
    )