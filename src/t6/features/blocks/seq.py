from dataclasses import dataclass
from typing import Dict

from .utils import clean_seq, AA20

# NOTE: stubs for now — you will fill with real AAC/DPC/QSO implementations.

@dataclass(frozen=True)
class AACBlock:
    name: str = "aac"
    def transform_one(self, seq: str) -> Dict[str, float]:
        s = clean_seq(seq)
        L = len(s)
        out = {f"AAC_{aa}": 0.0 for aa in AA20}
        if L == 0:
            return out
        for c in s:
            out[f"AAC_{c}"] += 1.0
        for aa in AA20:
            out[f"AAC_{aa}"] /= L
        return out


@dataclass(frozen=True)
class DPCBlock:
    name: str = "dpc"
    def transform_one(self, seq: str) -> Dict[str, float]:
        s = clean_seq(seq)
        L = len(s)
        out = {f"DPC_{a}{b}": 0.0 for a in AA20 for b in AA20}
        if L < 2:
            return out
        for i in range(L - 1):
            out[f"DPC_{s[i]}{s[i+1]}"] += 1.0
        denom = (L - 1)
        for k in list(out.keys()):
            out[k] /= denom
        return out


@dataclass(frozen=True)
class QSOBlock:
    maxlag: int = 30
    weight: float = 0.1
    name: str = "qso"
    def transform_one(self, seq: str) -> Dict[str, float]:
        s = clean_seq(seq)
        if not s:
            return {}
        # Use propy3 as allowed by the assignment
        from propy.QuasiSequenceOrder import GetQuasiSequenceOrder
        d = GetQuasiSequenceOrder(s, maxlag=self.maxlag, weight=self.weight)
        return {f"QSO_{k}": float(v) for k, v in d.items()}
