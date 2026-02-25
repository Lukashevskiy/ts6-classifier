"""Feature extractor that aggregates feature blocks into a DataFrame."""
from dataclasses import dataclass
from typing import Dict, List, Sequence

import pandas as pd

from ..domain.records import SequenceRecord
from .types import FeatureBlock

@dataclass
class FeatureExtractor:
    """Aggregate multiple feature blocks and build tabular features."""
    blocks: Sequence[FeatureBlock]

    def transform_one(self, seq: str) -> Dict[str, float]:
        """Compute features for a single sequence, with collision checks."""
        feats: Dict[str, float] = {}
        for b in self.blocks:
            part = b.transform_one(seq)
            overlap = set(feats.keys()) & set(part.keys())
            if overlap:
                raise ValueError(f"Feature key collision in block '{b.name}': {sorted(overlap)[:5]} ...")
            feats.update(part)
        return {k: float(v) for k, v in feats.items()}

    def transform(self, records: List[SequenceRecord], include_seq: bool = False) -> pd.DataFrame:
        """Compute features for a list of records and return a stable DataFrame."""
        rows: List[Dict[str, float]] = []
        for r in records:
            feats = self.transform_one(r.seq)
            feats["id"] = r.id
            feats["label"] = int(r.label)
            if include_seq:
                feats["seq"] = r.seq
            rows.append(feats)

        df = pd.DataFrame(rows).fillna(0.0)

        base_cols = ["id", "label"] + (["seq"] if include_seq else [])
        feature_cols = sorted(c for c in df.columns if c not in set(base_cols))
        df = df[base_cols + feature_cols]

        df["label"] = df["label"].astype("int64")
        for c in feature_cols:
            df[c] = df[c].astype("float64")

        return df
