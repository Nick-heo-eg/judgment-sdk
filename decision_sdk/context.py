"""
Decision context tracking

Tracks: request_id, decision_depth, ml_invoked, layers_skipped
"""

import uuid
from typing import List, Optional


class DecisionContext:
    """Tracks decision flow through layers."""

    def __init__(self, request_id: Optional[str] = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.decision_depth = 0
        self.ml_invoked = False
        self.layers_invoked: List[str] = []
        self.layers_skipped: List[str] = []
        self.dcl_state: Optional[str] = None
        self.dcp_action: Optional[str] = None

    def add_layer(self, layer_name: str):
        """Record layer invocation."""
        self.layers_invoked.append(layer_name)
        self.decision_depth += 1

    def skip_layer(self, layer_name: str):
        """Record layer bypass."""
        self.layers_skipped.append(layer_name)

    def set_ml_invoked(self):
        """Mark ML/LLM as invoked."""
        self.ml_invoked = True

    def to_dict(self):
        """Export context as dict."""
        return {
            "request_id": self.request_id,
            "decision_depth": self.decision_depth,
            "ml_invoked": self.ml_invoked,
            "layers_invoked": self.layers_invoked,
            "layers_skipped": self.layers_skipped,
            "dcl_state": self.dcl_state,
            "dcp_action": self.dcp_action
        }
