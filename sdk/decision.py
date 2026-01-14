"""
Decision Line (DCP) - Judgment checkpoint

Evaluates requests and returns ALLOW/HOLD/ESCALATE.
Default mode: ALLOW (safe mode - no blocking unless configured).
"""

from typing import Dict, List, Literal, Optional


DecisionType = Literal["ALLOW", "HOLD", "ESCALATE"]


class DecisionCheckpoint:
    """
    Judgment intervention point.

    Default behavior: ALLOW everything (safe mode).
    """

    def __init__(self, policy_rules: Optional[List[Dict]] = None, default_action: str = "ALLOW"):
        """
        Initialize decision checkpoint.

        Args:
            policy_rules: Optional list of policy rules
            default_action: Default when no rules match (default: "ALLOW")
        """
        self.policy_rules = policy_rules or []
        self.default_action = default_action

    def evaluate(self, request: Dict) -> Dict:
        """
        Evaluate request against policy rules.

        Returns:
            {
                "action": "ALLOW" | "HOLD" | "ESCALATE",
                "reason": str,
                "matched_rule": str | None
            }
        """
        # Check each policy rule
        for rule in self.policy_rules:
            if self._matches_rule(request, rule):
                return {
                    "action": rule["action"],
                    "reason": rule["reason"],
                    "matched_rule": rule["name"]
                }

        # No rule matched - return default
        return {
            "action": self.default_action,
            "reason": "No policy rule matched",
            "matched_rule": None
        }

    def _matches_rule(self, request: Dict, rule: Dict) -> bool:
        """Check if request matches a policy rule."""
        conditions = rule.get("conditions", {})

        for key, value in conditions.items():
            if request.get(key) != value:
                return False

        return True
