"""
Learning Line (DCL)

Replay-based structural learning.
NOT caching. Learns judgment structures.
"""

from typing import Dict, Tuple, Optional, Any


class DCL:
    """
    Decision Compression Layer

    Role: Learn judgment structures from DCP decisions
    Returns: ("hit"|"partial"|"miss", decision)
    Default: Conservative (threshold=3, learns on replay only)

    Key distinction: NOT cache
    - Cache stores: input → output
    - DCL stores: structure → decision
    """

    def __init__(self, confidence_threshold: int = 3):
        """
        Initialize DCL.

        Args:
            confidence_threshold: Number of consistent decisions before "hit"
        """
        self.confidence_threshold = confidence_threshold
        self.structure_memory: Dict[str, Dict[str, Any]] = {}

    def query(self, request: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        Query for learned structure.

        Args:
            request: Request data

        Returns:
            ("hit"|"partial"|"miss", decision)
            - "hit": High confidence, return decision
            - "partial": Learning in progress
            - "miss": No learned structure
        """
        structure_key = self._extract_structure(request)

        if structure_key not in self.structure_memory:
            return ("miss", None)

        entry = self.structure_memory[structure_key]
        confidence = entry["confidence"]
        decision = entry["decision"]

        if confidence >= self.confidence_threshold:
            return ("hit", decision)
        else:
            return ("partial", None)

    def learn(self, request: Dict[str, Any], decision: str):
        """
        Learn from DCP decision.

        This is REPLAY-BASED learning, not caching.
        Accumulates confidence for structure → decision mapping.
        """
        structure_key = self._extract_structure(request)

        if structure_key not in self.structure_memory:
            self.structure_memory[structure_key] = {
                "decision": decision,
                "confidence": 1
            }
        else:
            entry = self.structure_memory[structure_key]
            if entry["decision"] == decision:
                entry["confidence"] += 1
            else:
                # Conflicting decision - reset confidence
                entry["decision"] = decision
                entry["confidence"] = 1

    def _extract_structure(self, request: Dict[str, Any]) -> str:
        """
        Extract structural pattern from request.

        This is NOT input hashing. It's structural pattern extraction.
        Example: role(admin) + action(read) + resource(sensitive)
        """
        # Simple implementation: use category and sensitivity
        category = request.get("category", "unknown")
        sensitivity = request.get("sensitivity", "unknown")

        return f"struct:{category}:{sensitivity}"
