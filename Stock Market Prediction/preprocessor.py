import pandas as pd
from sklearn.preprocessing import StandardScaler

class Preprocessor:
    def __init__(self, feature_data: pd.DataFrame, target_data: pd.DataFrame):
        self.data = feature_data.copy()
        self.target_data = target_data.copy()

    def merge_features_and_target(self):
        self.data = self.data.merge(self.target_data[['Target']], left_index=True, right_index=True)
        return self

    def drop_missing(self):
        # Only drop rows where 'Target' is missing
        self.data = self.data[self.data['Target'].notna()]
        return self

    def scale_features(self, feature_cols=None):
        if feature_cols is None:
            feature_cols = self.data.columns.drop('Target')
        if len(self.data) > 0:   # only scale if there are rows
            scaler = StandardScaler()
            self.data[feature_cols] = scaler.fit_transform(self.data[feature_cols])
        return self

    def get_training_test_split(self, test_size: float = 0.2):
        if len(self.data) == 0:
            return pd.DataFrame(), pd.DataFrame()  # return empty DataFrames if no data
        split_index = int(len(self.data) * (1 - test_size))
        train = self.data.iloc[:split_index]
        test = self.data.iloc[split_index:]
        return train, test

