from pathlib import Path
from typing import Iterable, List, Tuple
import zipfile

from ..domain.records import SequenceRecord
from .fasta import read_fasta

def _score_path(path: Path, include: Iterable[str], exclude: Iterable[str]) -> int:
    name = path.as_posix().lower()
    score = 0
    for token in include:
        if token in name:
            score += 3
    for token in exclude:
        if token in name:
            score -= 2
    return score


def _pick_fasta(paths: List[Path], include: Iterable[str], exclude: Iterable[str], label: str) -> Path:
    if not paths:
        raise FileNotFoundError("No .fa/.fasta found after extracting zip")
    scored = [(p, _score_path(p, include, exclude)) for p in paths]
    scored.sort(key=lambda x: (x[1], x[0].as_posix()), reverse=True)
    best_score = scored[0][1]
    best = [p for p, s in scored if s == best_score and s > 0]
    if len(best) == 1:
        return best[0]
    if len(paths) == 2 and best_score <= 0:
        # Fall back to a simple 2-file dataset.
        return paths[0] if label == "pos" else paths[1]
    if best_score <= 0:
        raise RuntimeError(
            "Couldn't detect pos/neg FASTA. Rename files to include 'pos'/'neg' or update discovery."
        )
    raise RuntimeError(
        f"Ambiguous {label} FASTA candidates: {[p.as_posix() for p in best]}"
    )


def load_training_zip(zip_path: str | Path) -> Tuple[List[SequenceRecord], List[SequenceRecord]]:
    """
    Load Bastion6 training zip and return (positive_records, negative_records).

    Discovery rules:
    - Prefer files/paths containing pos|positive and neg|negative tokens.
    - If only two FASTA files exist, treat the first as pos and second as neg.
    """
    zip_path = Path(zip_path)
    extract_dir = zip_path.parent / (zip_path.stem + "_extracted")
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    fasta_files = sorted(
        list(extract_dir.rglob("*.fa")) + list(extract_dir.rglob("*.fasta"))
    )

    pos_path = _pick_fasta(
        fasta_files,
        include=("pos", "positive"),
        exclude=("neg", "negative"),
        label="pos",
    )
    neg_path = _pick_fasta(
        fasta_files,
        include=("neg", "negative"),
        exclude=("pos", "positive"),
        label="neg",
    )

    pos_records = [SequenceRecord(id=i, seq=s, label=1) for i, s in read_fasta(str(pos_path))]
    neg_records = [SequenceRecord(id=i, seq=s, label=0) for i, s in read_fasta(str(neg_path))]
    return pos_records, neg_records
