"""
Decision Line (DCP)

Judgment intervention: ALLOW / HOLD / SKIP
Default: ALLOW (safe mode)
"""

from typing import Dict, List, Optional, Any


class DCP:
    """
    Decision Checkpoint

    Role: Pre-invocation judgment
    Returns: ALLOW (proceed), HOLD (block), SKIP (not applicable)
    Default: ALLOW (safe mode - intervention possible but inactive)
    """

    def __init__(
        self,
        policy_rules: Optional[List[Dict]] = None,
        default_action: str = "ALLOW"
    ):
        """
        Initialize DCP.

        Args:
            policy_rules: List of policy rules (optional)
            default_action: Default action when no rules match (default: ALLOW)
        """
        self.policy_rules = policy_rules or []
        self.default_action = default_action

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate request against policy rules.

        Args:
            request: Request data

        Returns:
            {
                "action": "ALLOW" | "HOLD" | "SKIP",
                "reason": str,
                "matched_rule": str | None
            }
        """
        # Check each policy rule
        for rule in self.policy_rules:
            if self._matches_rule(request, rule):
                return {
                    "action": rule["action"],
                    "reason": rule.get("reason", f"Matched rule: {rule['name']}"),
                    "matched_rule": rule["name"]
                }

        # No rules matched - return default action
        return {
            "action": self.default_action,
            "reason": "No matching rules, default action applied",
            "matched_rule": None
        }

    def _matches_rule(self, request: Dict[str, Any], rule: Dict) -> bool:
        """Check if request matches rule conditions."""
        conditions = rule.get("conditions", {})

        for key, expected_value in conditions.items():
            if key not in request:
                return False
            if request[key] != expected_value:
                return False

        return True
