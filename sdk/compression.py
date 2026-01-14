"""
Learning Line (DCL) - Pattern learning

Learns judgment structures to reduce decision depth.
Default mode: Conservative (high confidence threshold).
"""

from typing import Dict, Tuple, Optional, Literal


MatchType = Literal["hit", "partial", "miss"]


class CompressionLayer:
    """
    Judgment structure learning.

    Default behavior: Conservative (requires multiple observations for hit).
    """

    def __init__(self, confidence_threshold: int = 3):
        """
        Initialize compression layer.

        Args:
            confidence_threshold: Number of observations needed for hit (default: 3)
        """
        self.confidence_threshold = confidence_threshold
        self.structures = {}  # {structure_key: (decision, confidence)}

    def query(self, request: Dict) -> Tuple[MatchType, Optional[str]]:
        """
        Query for learned structure.

        Returns:
            (match_type, decision)
            - "hit": High-confidence match, decision returned
            - "partial": Low-confidence match, forward to DCP
            - "miss": No match, forward to DCP
        """
        structure = self._extract_structure(request)

        if structure in self.structures:
            decision, confidence = self.structures[structure]

            if confidence >= self.confidence_threshold:
                return ("hit", decision)
            else:
                return ("partial", None)

        return ("miss", None)

    def learn(self, request: Dict, decision: str):
        """Learn from DCP decision."""
        structure = self._extract_structure(request)

        if structure in self.structures:
            prev_decision, confidence = self.structures[structure]

            if prev_decision == decision:
                self.structures[structure] = (decision, confidence + 1)
            else:
                # Conflicting decision - reset
                self.structures[structure] = (decision, 1)
        else:
            self.structures[structure] = (decision, 1)

    def _extract_structure(self, request: Dict) -> str:
        """
        Extract relational structure from request.

        Example: category:hr|action:query|sensitivity:high
        """
        components = []

        for key in ["category", "action", "sensitivity", "resource_type", "role"]:
            if key in request:
                components.append(f"{key}:{request[key]}")

        return "|".join(components) if components else "default"
