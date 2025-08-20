import yfinance as yf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class PredictionPipeline:
    def __init__(self, tickers=None, lookback=60):
        """
        tickers: dict of index names to Yahoo Finance symbols
        lookback: number of past days to use for training
        """
        if tickers is None:
            self.tickers = {
                "NASDAQ": "^IXIC",
                "Dow Jones": "^DJI",
                "S&P500": "^GSPC"
            }
        else:
            self.tickers = tickers

        self.lookback = lookback

    def _get_data(self, symbol):
        """Download historical price data and compute features."""
        df = yf.download(symbol, period="6mo", interval="1d")
        df = df.dropna()

        # Daily return
        df["Return"] = df["Close"].pct_change()

        # Next-day direction (1 = up, 0 = down)
        df["Target"] = (df["Return"].shift(-1) > 0).astype(int)

        df = df.dropna()
        return df

    def _train_and_predict(self, df):
        """Train logistic regression and predict tomorrow."""
        X = df[["Return"]]
        y = df["Target"]

        # Use a sklearn pipeline for scaling + LR
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression())
        ])

        # Train on last N days
        X_train, y_train = X[-self.lookback:], y[-self.lookback:]
        model.fit(X_train, y_train)

        # Predict tomorrow (last row)
        tomorrow_pred = model.predict(X.tail(1))[0]
        return int(tomorrow_pred)

    def run(self):
        """Run pipeline for all tickers and return predictions dict."""
        predictions = {}
        for name, symbol in self.tickers.items():
            df = self._get_data(symbol)
            pred = self._train_and_predict(df)
            predictions[name] = pred
        return predictions


if __name__ == "__main__":
    pipeline = PredictionPipeline()
    preds = pipeline.run()
    print("Predictions:", preds)
