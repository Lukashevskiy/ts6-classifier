
AA20 = "ACDEFGHIKLMNPQRSTVWY"
AA20_SET = set(AA20)

def clean_seq(seq: str) -> str:
    """Keep only 20 standard amino acids."""
    seq = seq.upper()
    return "".join([c for c in seq if c in AA20_SET])
