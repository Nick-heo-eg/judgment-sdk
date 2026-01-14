"""
Single entry point: wrap(callable)

Usage:
    from decision_sdk import wrap

    result = wrap(your_llm_function)(request)
"""

from typing import Callable, Dict, Any, Optional
from .context import DecisionContext
from .audit.ajt import AJT
from .decision.dcp import DCP
from .learning.dcl import DCL
from .config import DEFAULT_CONFIG


class DecisionWrapper:
    """Wraps LLM calls with decision products."""

    def __init__(
        self,
        llm_callable: Callable,
        config: Optional[Dict] = None
    ):
        self.llm_callable = llm_callable
        self.config = config or DEFAULT_CONFIG

        # Initialize products based on config
        ajt_config = self.config["ajt"]
        dcp_config = self.config["dcp"]
        dcl_config = self.config["dcl"]

        self.ajt = AJT(log_path=ajt_config["log_path"]) if ajt_config["enabled"] else None

        self.dcp = DCP(
            policy_rules=dcp_config["policy_rules"],
            default_action=dcp_config["default_action"]
        ) if dcp_config["enabled"] else None

        self.dcl = DCL(
            confidence_threshold=dcl_config["confidence_threshold"]
        ) if dcl_config["enabled"] else None

    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute wrapped LLM call.

        Flow: DCL → DCP → [conditional] LLM → AJT

        Returns:
            {
                "response": ...,
                "metadata": {
                    "request_id": str,
                    "decision_depth": int,
                    "ml_invoked": bool,
                    "layers_invoked": List[str],
                    "layers_skipped": List[str],
                    "dcl_state": str | None,
                    "dcp_action": str
                }
            }
        """
        ctx = DecisionContext()

        # Layer 1: DCL (if enabled)
        if self.dcl:
            ctx.add_layer("DCL")
            dcl_match, dcl_decision = self.dcl.query(request)
            ctx.dcl_state = dcl_match

            if dcl_match == "hit":
                # DCL hit - skip DCP and LLM
                ctx.skip_layer("DCP")
                ctx.skip_layer("LLM")
                final_response = {"decision": dcl_decision, "source": "DCL"}

                # Log and return
                if self.ajt:
                    self.ajt.log(ctx.request_id, request, final_response, ctx.to_dict())

                return {
                    "response": final_response,
                    "metadata": ctx.to_dict()
                }

        # Layer 2: DCP (if enabled)
        if self.dcp:
            ctx.add_layer("DCP")
            dcp_result = self.dcp.evaluate(request)
            ctx.dcp_action = dcp_result["action"]

            if dcp_result["action"] == "ALLOW":
                # Layer 3: LLM invocation
                ctx.add_layer("LLM")
                ctx.set_ml_invoked()

                llm_response = self.llm_callable(request)
                final_response = llm_response

                # DCL learns from DCP
                if self.dcl:
                    self.dcl.learn(request, "ALLOW")

            else:  # HOLD or SKIP
                # Skip LLM
                ctx.skip_layer("LLM")
                final_response = {
                    "decision": dcp_result["action"],
                    "reason": dcp_result["reason"]
                }

                # DCL learns from DCP
                if self.dcl:
                    self.dcl.learn(request, dcp_result["action"])

        else:
            # No DCP - direct LLM call
            ctx.add_layer("LLM")
            ctx.set_ml_invoked()
            final_response = self.llm_callable(request)

        # Log decision
        if self.ajt:
            self.ajt.log(ctx.request_id, request, final_response, ctx.to_dict())

        return {
            "response": final_response,
            "metadata": ctx.to_dict()
        }


def wrap(llm_callable: Callable, config: Optional[Dict] = None) -> DecisionWrapper:
    """
    Wrap your LLM callable with decision products.

    Args:
        llm_callable: Your LLM function (takes request dict, returns response dict)
        config: Optional configuration (defaults to safe mode)

    Returns:
        DecisionWrapper that can be called with request dict

    Example:
        from decision_sdk import wrap

        def my_llm(request):
            return {"text": f"Response to: {request['prompt']}"}

        wrapped_llm = wrap(my_llm)
        result = wrapped_llm({"prompt": "Hello"})

        print(result["metadata"]["ml_invoked"])  # True or False
    """
    return DecisionWrapper(llm_callable, config)
