"""
Default configuration: Safe mode

- AJT: Always records (observe only)
- DCP: Default ALLOW (intervention possible but inactive)
- DCL: Conservative learning (threshold=3, learns on replay only)
"""

DEFAULT_CONFIG = {
    "ajt": {
        "enabled": True,
        "log_path": "audit_trail.jsonl"
    },
    "dcp": {
        "enabled": True,
        "default_action": "ALLOW",
        "policy_rules": []
    },
    "dcl": {
        "enabled": False,  # Off by default
        "confidence_threshold": 3,
        "learn_mode": "replay"  # Only learns from DCP decisions
    }
}
