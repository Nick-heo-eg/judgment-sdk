"""
Responsible AI Client

Unified client that wraps your LLM calls with AJT/DCP/DCL.

Flow: Request → DCL → DCP → LLM → AJT logging
"""

from typing import Dict, Callable, Optional, Any
try:
    from .audit import AuditLogger
    from .decision import DecisionCheckpoint
    from .compression import CompressionLayer
except ImportError:
    from audit import AuditLogger
    from decision import DecisionCheckpoint
    from compression import CompressionLayer
import uuid


class ResponsibleAIClient:
    """
    Wrap your LLM calls with responsible AI products.

    Default mode: Safe (AJT logs, DCP ALLOW, DCL conservative)
    """

    def __init__(
        self,
        audit_logger: Optional[AuditLogger] = None,
        decision_checkpoint: Optional[DecisionCheckpoint] = None,
        compression_layer: Optional[CompressionLayer] = None
    ):
        """
        Initialize responsible AI client.

        Args:
            audit_logger: Optional AuditLogger (default: auto-created)
            decision_checkpoint: Optional DecisionCheckpoint (default: ALLOW-only)
            compression_layer: Optional CompressionLayer (default: None)
        """
        self.audit = audit_logger or AuditLogger()
        self.decision = decision_checkpoint or DecisionCheckpoint()
        self.compression = compression_layer  # Optional

    def call(
        self,
        llm_function: Callable,
        request: Dict,
        request_id: Optional[str] = None
    ) -> Dict:
        """
        Wrap LLM call with responsible AI products.

        Args:
            llm_function: Your LLM calling function (takes request dict, returns response dict)
            request: Request data
            request_id: Optional request ID (auto-generated if not provided)

        Returns:
            {
                "response": LLM response,
                "metadata": {
                    "request_id": str,
                    "decision_depth": int,
                    "dcl_state": str | None,
                    "dcp_action": str,
                    "ml_invoked": bool,
                    "ajt_logged": bool
                }
            }
        """
        request_id = request_id or str(uuid.uuid4())

        layers_invoked = []
        layers_skipped = []
        ml_invoked = False
        decision_depth = 0

        # Layer 1: DCL (if enabled)
        dcl_state = None
        if self.compression:
            layers_invoked.append("DCL")
            decision_depth += 1

            dcl_match, dcl_decision = self.compression.query(request)
            dcl_state = dcl_match

            if dcl_match == "hit":
                # DCL returned decision - skip DCP and LLM
                final_response = {"decision": dcl_decision, "source": "DCL"}
                layers_skipped.extend(["DCP", "LLM"])

                # Log and return
                self._log_decision(
                    request_id, request, final_response,
                    decision_depth, layers_invoked, layers_skipped,
                    ml_invoked, dcl_state, None
                )

                return {
                    "response": final_response,
                    "metadata": {
                        "request_id": request_id,
                        "decision_depth": decision_depth,
                        "dcl_state": dcl_state,
                        "dcp_action": None,
                        "ml_invoked": ml_invoked,
                        "ajt_logged": True
                    }
                }

        # Layer 2: DCP (always invoked unless DCL hit)
        layers_invoked.append("DCP")
        decision_depth += 1

        dcp_result = self.decision.evaluate(request)
        dcp_action = dcp_result["action"]

        if dcp_action == "ALLOW":
            # Layer 3: LLM invocation
            layers_invoked.append("LLM")
            decision_depth += 1
            ml_invoked = True

            llm_response = llm_function(request)
            final_response = llm_response

            # DCL learns from DCP
            if self.compression:
                self.compression.learn(request, "ALLOW")

        else:  # HOLD or ESCALATE
            # Skip LLM
            final_response = {"decision": dcp_action, "reason": dcp_result["reason"]}
            layers_skipped.append("LLM")

            # DCL learns from DCP
            if self.compression:
                self.compression.learn(request, dcp_action)

        # Log decision
        self._log_decision(
            request_id, request, final_response,
            decision_depth, layers_invoked, layers_skipped,
            ml_invoked, dcl_state, dcp_action
        )

        return {
            "response": final_response,
            "metadata": {
                "request_id": request_id,
                "decision_depth": decision_depth,
                "dcl_state": dcl_state,
                "dcp_action": dcp_action,
                "ml_invoked": ml_invoked,
                "ajt_logged": True
            }
        }

    def _log_decision(
        self,
        request_id: str,
        request: Dict,
        response: Dict,
        decision_depth: int,
        layers_invoked: list,
        layers_skipped: list,
        ml_invoked: bool,
        dcl_state: Optional[str],
        dcp_action: Optional[str]
    ):
        """Log decision to AJT."""
        metadata = {
            "decision_depth": decision_depth,
            "layers_invoked": layers_invoked,
            "layers_skipped": layers_skipped,
            "ml_invoked": ml_invoked,
            "dcl_state": dcl_state,
            "dcp_action": dcp_action,
            "ajt_logged": True
        }

        self.audit.log(request_id, request, response, metadata)
