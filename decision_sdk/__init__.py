"""
Judgment SDK

Single entry point: wrap(callable)

Default mode: Safe
- AJT: Always records judgments
- DCP: Default ALLOW (judgment possible but inactive)
- DCL: Learns judgment structures on replay only
"""

from .wrap import wrap

__version__ = "0.1.0"
__all__ = ["wrap"]
