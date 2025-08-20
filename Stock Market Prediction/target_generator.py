import pandas as pd
import numpy as np

class TargetGenerator:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def add_binary_target(self, days_ahead=30, target_col="Target"):
        self.data[target_col] = (self.data["Close"].shift(-days_ahead) > self.data["Close"]).astype(int)
        return self

    def add_multiclass_target(self, days_ahead=30, thresholds=[0.01, 0.02], target_col="Target"):
        """
        thresholds = [up_threshold, down_threshold]
        Assign:
            1: price increase > up_threshold
            0: price change within ±down_threshold
           -1: price decrease > down_threshold
        """
        future_return = (self.data["Close"].shift(-days_ahead) - self.data["Close"]) / self.data["Close"]
        up_threshold, down_threshold = thresholds
        conditions = [
            future_return > up_threshold,
            future_return < -down_threshold
        ]
        choices = [1, -1]
        self.data[target_col] = np.select(conditions, choices, default=0)
        return self

    def get_data(self):
        return self.data


        

