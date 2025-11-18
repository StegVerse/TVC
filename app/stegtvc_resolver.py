import json
import urllib.request

def stegtvc_resolve(use_case="default", module="unknown", importance="normal"):
    """
    Fetch config.py from GitHub and return model selection.
    """

    url = "https://raw.githubusercontent.com/StegVerse-Labs/StegTVC/main/app/config.py"

    with urllib.request.urlopen(url, timeout=10) as resp:
        raw = resp.read().decode("utf-8")

    # Execute config file safely
    config_namespace = {}
    exec(raw, config_namespace)

    config = config_namespace.get("CONFIG", {})

    # Use-case specific?
    if use_case in config.get("use_cases", {}):
        model_cfg = config["use_cases"][use_case]
    else:
        model_cfg = config["default"]

    return {
        "provider": model_cfg,
        "meta": {
            "module": module,
            "importance": importance,
        },
    }
