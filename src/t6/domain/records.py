"""Data structures for sequence records."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SequenceRecord:
    """A labeled protein sequence record."""
    id: str
    seq: str
    label: int  # 1 pos, 0 neg
