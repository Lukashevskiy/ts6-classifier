from pathlib import Path
import pandas as pd

from t6.io.dataset import load_training_zip
from t6.features.extractor import FeatureExtractor
from t6.features.blocks.seq import AACBlock, DPCBlock, QSOBlock
from t6.features.blocks.ctd import CTDCBlock, CTDTBlock
from t6.pipeline.export import save_table

def main():
    zip_path = Path("data/T6SE_training_data.zip")
    if not zip_path.exists():
        raise FileNotFoundError("Put T6SE_training_data.zip into data/")

    pos, neg = load_training_zip(zip_path)

    extractor = FeatureExtractor(blocks=[
        AACBlock(),
        DPCBlock(),
        CTDCBlock(),
        CTDTBlock(),
        # QSOBlock(),  # enable if needed
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

    print("Saved CSV/TSV to out/")

if __name__ == "__main__":
    main()
