"""
Audit Line (AJT)

Observation only. Records everything, decides nothing.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any


class AJT:
    """
    Audit Line - Observation only

    Role: Record request/response/decision metadata
    Does NOT: Make decisions, intervene, or modify behavior
    """

    def __init__(self, log_path: str = "audit_trail.jsonl"):
        self.log_path = log_path

    def log(
        self,
        request_id: str,
        request_data: Dict[str, Any],
        response_data: Dict[str, Any],
        decision_metadata: Dict[str, Any]
    ):
        """
        Log request/response/decision.

        This is OBSERVATION ONLY. No decision-making.
        """
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "request": request_data,
            "response": response_data,
            "decision_metadata": decision_metadata
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
