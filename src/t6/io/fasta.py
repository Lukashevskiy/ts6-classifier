from typing import List, Tuple
from Bio import SeqIO

def read_fasta(path: str) -> List[Tuple[str, str]]:
    """Return list of (id, sequence) from a FASTA file."""
    out: List[Tuple[str, str]] = []
    for rec in SeqIO.parse(path, "fasta"):
        out.append((rec.id, str(rec.seq)))
    return out
