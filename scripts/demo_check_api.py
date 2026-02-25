from t6.domain.records import SequenceRecord
from t6.features.extractor import FeatureExtractor
from t6.features.blocks.seq import AACBlock, DPCBlock
from t6.features.blocks.ctd import CTDCBlock, CTDTBlock

def main():
    records = [
        SequenceRecord(id="p1", seq="MKKAAAWT", label=1),
        SequenceRecord(id="n1", seq="GGGTTT---XX", label=0),
    ]
    extractor = FeatureExtractor(blocks=[AACBlock(), DPCBlock(), CTDCBlock(), CTDTBlock()])
    df = extractor.transform(records)
    print(df.head())
    print("shape:", df.shape)

if __name__ == "__main__":
    main()
