class StockPredictionPipeline:
    def __init__(self, feature_class, target_class, preprocessor_class, model_class):
        self.feature_class = feature_class
        self.target_class = target_class
        self.preprocessor_class = preprocessor_class
        self.model_class = model_class

    def run_pipeline(
        self,
        raw_data,
        lag_days=[1, 2],
        ma_days=[5],
        volatility_days=[5],
        target_days_ahead=30
    ):
        # Step 1: Feature engineering
        fe = self.feature_class(raw_data)
        fe.compute_daily_returns()\
          .add_moving_average_column(ma_days)\
          .lag_features(lag_days)\
          .compute_rolling_volatility(volatility_days)
        feature_data = fe.data

        # Step 2: Target generation
        tg = self.target_class(feature_data)
        tg.add_binary_target(days_ahead=target_days_ahead)
        target_data = tg.get_data()

        # Step 3: Preprocessing
        pre = self.preprocessor_class(feature_data, target_data)
        pre.merge_features_and_target().drop_missing().scale_features()
        train, test = pre.get_training_test_split(test_size=0.2)

        # Step 4: Model training
        if len(train) == 0 or len(test) == 0:
            print("Warning: Not enough data after preprocessing. Skipping model training.")
            return train, test, None

        model_trainer = self.model_class(train, test)
        model_trainer.train_model().predict().evaluate()
        return train, test, model_trainer






    