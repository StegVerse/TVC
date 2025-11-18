"""
StegTVC Core v1.0 — Model Routing Configuration
This file tells all StegVerse AI entities which model/provider to use.
"""

CONFIG = {
    "default": {
        "provider": "github-models",
        "model": "gpt-5-mini",  # safe, cheap, always available fallback
    },

    "use_cases": {
        "code-review": {
            "provider": "github-models",
            "model": "gpt-5",
        },

        "connectivity-check": {
            "provider": "github-models",
            "model": "gpt-5-mini",
        },

        "documentation": {
            "provider": "github-models",
            "model": "gpt-4o-mini",
        },
    }
}
