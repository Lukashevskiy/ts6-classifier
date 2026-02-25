"""Type definitions for feature blocks."""
from typing import Dict, Protocol

class FeatureBlock(Protocol):
    """Protocol for a feature block used by FeatureExtractor."""
    name: str
    def transform_one(self, seq: str) -> Dict[str, float]: ...
