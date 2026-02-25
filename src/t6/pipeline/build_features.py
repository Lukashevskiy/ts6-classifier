import pandas as pd
from typing import List

from ..domain.records import SequenceRecord
from ..features.extractor import FeatureExtractor

def build_features_df(records: List[SequenceRecord], extractor: FeatureExtractor, include_seq: bool = False) -> pd.DataFrame:
    return extractor.transform(records, include_seq=include_seq)
