import pandas as pd
import numpy as np

class FeatureEngineering:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def compute_daily_returns(self):
        self.data["Daily Return"] = self.data["Close"].pct_change()
        return self

    def add_moving_average_column(self, windows=[5, 10, 20]):
        if isinstance(windows, int):
            windows = [windows]
        for n in windows:
            self.data[f"MA_{n}"] = self.data["Close"].rolling(window=n).mean()
        return self


    
    def lag_features(self, t):
        """
        Add lag features.
        t can be an int (single lag) or list of ints (multiple lags)
        """
        if isinstance(t, int):
            self.data[f"Lag{t}"] = self.data["Close"].shift(t)
        elif isinstance(t, list):
            for lag in t:
                self.data[f"Lag{lag}"] = self.data["Close"].shift(lag)
        else:
            raise ValueError("t must be int or list of ints")
        return self

    def compute_rolling_volatility(self, windows=[5, 10, 20]):
        self.compute_daily_returns()
        if isinstance(windows, int):
            windows = [windows]
        for t in windows:
            self.data[f"Vol_{t}"] = self.data["Daily Return"].rolling(window=t).std()
        return self


    def add_rsi(self, period=14):
        delta = self.data['Close'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=period).mean()
        avg_loss = pd.Series(loss).rolling(window=period).mean()
        rs = avg_gain / avg_loss
        self.data[f'RSI_{period}'] = 100 - (100 / (1 + rs))
        return self

    def add_bollinger_bands(self, window=20, n_std=2):
        rolling_mean = self.data['Close'].rolling(window).mean()
        rolling_std = self.data['Close'].rolling(window).std()
        self.data[f'BB_upper_{window}'] = rolling_mean + (rolling_std * n_std)
        self.data[f'BB_lower_{window}'] = rolling_mean - (rolling_std * n_std)
        return self

    def add_macd(self, short_window=12, long_window=26, signal_window=9):
        ema_short = self.data['Close'].ewm(span=short_window, adjust=False).mean()
        ema_long = self.data['Close'].ewm(span=long_window, adjust=False).mean()
        macd = ema_short - ema_long
        signal = macd.ewm(span=signal_window, adjust=False).mean()
        self.data['MACD'] = macd
        self.data['MACD_signal'] = signal
        return self

    def get_data(self):
        return self.data



