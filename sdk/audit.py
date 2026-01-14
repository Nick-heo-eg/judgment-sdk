"""
Audit Line (AJT) - Observation only

Records all requests/responses without making decisions.
Zero configuration required - just logs everything.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Optional


class AuditLogger:
    """
    Observation-only logger.

    Default behavior: Record everything, decide nothing.
    """

    def __init__(self, log_path: str = "audit_trail.jsonl", auto_save: bool = True):
        """
        Initialize audit logger.

        Args:
            log_path: Path to JSONL log file
            auto_save: If True, saves immediately after each log (default: True)
        """
        self.log_path = log_path
        self.auto_save = auto_save
        self.logs = []

    def log(
        self,
        request_id: str,
        request_data: Dict,
        response_data: Dict,
        decision_metadata: Optional[Dict] = None
    ):
        """
        Record a single request/response pair.

        This method does NOT make decisions - it only observes.
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "request": request_data,
            "response": response_data,
            "decision_metadata": decision_metadata or {}
        }

        self.logs.append(entry)

        if self.auto_save:
            self._save_entry(entry)

    def _save_entry(self, entry: Dict):
        """Append single entry to log file."""
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def save_all(self):
        """Save all logs (used when auto_save=False)."""
        with open(self.log_path, 'w') as f:
            for entry in self.logs:
                f.write(json.dumps(entry) + '\n')
