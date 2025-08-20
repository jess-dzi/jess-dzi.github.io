from download_data import DataDownloader
from feature_engineering import FeatureEngineering
from target_generator import TargetGenerator
from preprocessor import Preprocessor
from model_training import ModelTrainer
from stock_pipeline import StockPredictionPipeline
from prediction_pipeline import PredictionPipeline
from chart_generator import ChartGenerator

if __name__ == "__main__":
    # 1. Run pipeline to get predictions
    pipeline = PredictionPipeline()
    predictions = pipeline.run()  # {"NASDAQ": 1, "Dow Jones": 0, "S&P500": 1}

    # 2. Map indices to tickers
    index_symbols = {
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "S&P500": "^GSPC"
    }

    # 3. Combine ticker + prediction
    index_predictions = {name: (index_symbols[name], pred) for name, pred in predictions.items()}

    # 4. Generate charts & dashboard JSON
    generator = ChartGenerator()
    dashboard_data = generator.generate_all(index_predictions)

    print("Charts and JSON ready!")
    print(dashboard_data)
