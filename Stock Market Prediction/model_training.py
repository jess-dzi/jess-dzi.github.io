from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class ModelTrainer:
    def __init__(self, train_data, test_data, target_col='Target'):
        self.train = train_data
        self.test = test_data
        self.target_col = target_col
        self.model = RandomForestClassifier(
            n_estimators=200, 
            random_state=42, 
            class_weight='balanced'  # handle class imbalance
        )

    def train_model(self):
        self.model.fit(
            self.train.drop(columns=[self.target_col]), 
            self.train[self.target_col]
        )
        return self

    def predict(self):
        self.predictions = self.model.predict(
            self.test.drop(columns=[self.target_col])
        )
        return self

    def evaluate(self):
        print("Accuracy:", accuracy_score(self.test[self.target_col], self.predictions))
        print(classification_report(self.test[self.target_col], self.predictions))
        return self

    def get_predictions(self):
        return self.predictions, self.test[self.target_col]
