import yfinance as yf
import pandas as pd

class DataDownloader:
    def __init__(self, tickers: dict, period: str = "1y"):
        self.tickers = tickers
        self.period = period
        self.data = {}

    def download(self):
        for name, symbol in self.tickers.items():
            ticker = yf.Ticker(symbol)
            self.data[name] = ticker.history(period=self.period)
        return self

    def get_data(self):
        return self.data



