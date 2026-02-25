from pathlib import Path
from typing import List, Tuple
import zipfile

from ..domain.records import SequenceRecord
from .fasta import read_fasta

def _list_fasta_files(extract_dir: Path) -> List[Path]:
    """List real FASTA files only (skip macOS metadata and hidden files)."""
    out: List[Path] = []
    for p in extract_dir.rglob("*.fasta"):
        if not p.is_file():
            continue
        if "__MACOSX" in p.parts:
            continue
        if p.name.startswith(".") or p.name.startswith("._"):
            continue
        out.append(p)
    return sorted(out)


def _pick_pos_neg(paths: List[Path]) -> Tuple[Path, Path]:
    if not paths:
        raise FileNotFoundError("No *.fasta files found after extracting zip")

    pos_candidates = [p for p in paths if "pos" in p.name.lower()]
    neg_candidates = [p for p in paths if "neg" in p.name.lower()]

    if len(pos_candidates) == 1 and len(neg_candidates) == 1:
        return pos_candidates[0], neg_candidates[0]

    if len(paths) == 2:
        a, b = paths
        if "pos" in a.name.lower() or "neg" in b.name.lower():
            return a, b
        if "neg" in a.name.lower() or "pos" in b.name.lower():
            return b, a
        return a, b

    raise RuntimeError(
        "Cannot uniquely detect positive/negative FASTA files. "
        f"Detected: {[p.as_posix() for p in paths]}"
    )


def load_training_zip(zip_path: str | Path) -> Tuple[List[SequenceRecord], List[SequenceRecord]]:
    """
    Load Bastion6 training zip and return (positive_records, negative_records).

    Discovery rules:
    - Use only *.fasta files from extracted content.
    - Skip metadata/hidden files (e.g. __MACOSX, ._*).
    - Detect pos/neg by filename tokens; if exactly 2 files exist, use those.
    """
    zip_path = Path(zip_path)
    extract_dir = zip_path.parent / (zip_path.stem + "_extracted")
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    fasta_files = _list_fasta_files(extract_dir)
    pos_path, neg_path = _pick_pos_neg(fasta_files)

    pos_records = [SequenceRecord(id=i, seq=s, label=1) for i, s in read_fasta(str(pos_path))]
    neg_records = [SequenceRecord(id=i, seq=s, label=0) for i, s in read_fasta(str(neg_path))]
    return pos_records, neg_records
