from pathlib import Path
import pandas as pd

from t6.io.dataset import load_training_zip
from t6.features.extractor import FeatureExtractor
from t6.features.blocks.seq import AACBlock, DPCBlock, QSOBlock
from t6.features.blocks.ctd import CTDCBlock, CTDTBlock
from t6.pipeline.export import save_table


FEATURE_GROUPS = {
    "aac": ("AAC_",),
    "dpc": ("DPC_",),
    "qso": ("QSO_",),
    "ctdc": ("CTDC_",),
    "ctdt": ("CTDT_",),
}


def _select_group(df: pd.DataFrame, prefixes: tuple[str, ...]) -> pd.DataFrame:
    base = ["id", "label"]
    cols = [c for c in df.columns if c.startswith(prefixes)]
    return df[base + cols]

def main():
    zip_path = Path("data/t6se-training-data.zip")
    if not zip_path.exists():
        raise FileNotFoundError("Put T6SE_training_data.zip into data/")

    pos, neg = load_training_zip(zip_path)

    extractor = FeatureExtractor(blocks=[
        AACBlock(),
        DPCBlock(),
        CTDCBlock(),
        CTDTBlock(),
        QSOBlock(),
    ])

    df_pos = extractor.transform(pos)
    df_neg = extractor.transform(neg)
    df_all = pd.concat([df_pos, df_neg], ignore_index=True)

    save_table(df_pos, "out/positive_features.csv", sep=",")
    save_table(df_neg, "out/negative_features.csv", sep=",")
    save_table(df_all, "out/all_features.csv", sep=",")

    save_table(df_pos, "out/positive_features.tsv", sep="\t")
    save_table(df_neg, "out/negative_features.tsv", sep="\t")
    save_table(df_all, "out/all_features.tsv", sep="\t")

    # Per-feature exports for assignment report
    for group_name, prefixes in FEATURE_GROUPS.items():
        gpos = _select_group(df_pos, prefixes)
        gneg = _select_group(df_neg, prefixes)
        gall = _select_group(df_all, prefixes)

        save_table(gpos, f"out/positive_{group_name}.csv", sep=",")
        save_table(gneg, f"out/negative_{group_name}.csv", sep=",")
        save_table(gall, f"out/all_{group_name}.csv", sep=",")

        save_table(gpos, f"out/positive_{group_name}.tsv", sep="\t")
        save_table(gneg, f"out/negative_{group_name}.tsv", sep="\t")
        save_table(gall, f"out/all_{group_name}.tsv", sep="\t")

    print("Saved all feature tables to out/")

if __name__ == "__main__":
    main()
