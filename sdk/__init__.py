"""
Responsible AI SDK

Three independently usable products:
- audit: Audit Line (AJT) - observation only
- decision: Decision Line (DCP) - judgment checkpoint
- compression: Learning Line (DCL) - pattern learning

Default mode: Safe (observation, ALLOW-only, conservative learning)
"""

from .audit import AuditLogger
from .decision import DecisionCheckpoint
from .compression import CompressionLayer
from .client import ResponsibleAIClient

__version__ = "0.1.0"

__all__ = [
    "AuditLogger",
    "DecisionCheckpoint",
    "CompressionLayer",
    "ResponsibleAIClient"
]
