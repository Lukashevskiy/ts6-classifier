from dataclasses import dataclass
from typing import Dict, Tuple

from .utils import clean_seq

# 7 physicochemical properties in CTD-style grouping (3 groups each).
CTD_GROUPS: Dict[str, Tuple[set, set, set]] = {
    "hydrophobicity": (set("RKEDQN"), set("GASTPHY"), set("CLVIMFW")),
    "polarity": (set("LIFWCMVY"), set("PATGS"), set("HQRKNED")),
    "charge": (set("KR"), set("ANCQGHILMFPSTWYV"), set("DE")),
    "secondary_structure": (set("EALMQKRH"), set("VIYCWFT"), set("GNPSD")),
    "solvent_accessibility": (set("ALFCGIVW"), set("RKQEND"), set("MSPTHY")),
    "polarizability": (set("GASDT"), set("CPNVEQIL"), set("KMHFRYW")),
    "vdw_volume": (set("GASTPDC"), set("NVEQIL"), set("MHKFRYW")),
}

def _gid(aa: str, groups: Tuple[set, set, set]) -> int:
    g1, g2, g3 = groups
    if aa in g1: return 1
    if aa in g2: return 2
    if aa in g3: return 3
    return 0


@dataclass(frozen=True)
class CTDCBlock:
    name: str = "ctdc"
    def transform_one(self, seq: str) -> Dict[str, float]:
        s = clean_seq(seq)
        L = len(s)
        out: Dict[str, float] = {}
        for prop, groups in CTD_GROUPS.items():
            counts = [0, 0, 0]
            if L:
                for aa in s:
                    g = _gid(aa, groups)
                    if g:
                        counts[g-1] += 1
            for i in range(3):
                out[f"CTDC_{prop}_G{i+1}"] = (counts[i] / L) if L else 0.0
        return out


@dataclass(frozen=True)
class CTDTBlock:
    name: str = "ctdt"
    def transform_one(self, seq: str) -> Dict[str, float]:
        s = clean_seq(seq)
        L = len(s)
        out: Dict[str, float] = {}
        for prop, groups in CTD_GROUPS.items():
            t12 = t13 = t23 = 0
            if L >= 2:
                for i in range(L - 1):
                    a = _gid(s[i], groups)
                    b = _gid(s[i+1], groups)
                    if a == 0 or b == 0:
                        continue
                    x, y = sorted((a, b))
                    if (x, y) == (1, 2): t12 += 1
                    elif (x, y) == (1, 3): t13 += 1
                    elif (x, y) == (2, 3): t23 += 1
            denom = (L - 1) if L >= 2 else 1
            out[f"CTDT_{prop}_12"] = t12 / denom
            out[f"CTDT_{prop}_13"] = t13 / denom
            out[f"CTDT_{prop}_23"] = t23 / denom
        return out
