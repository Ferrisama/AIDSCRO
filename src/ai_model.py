import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score


class TrafficPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_importance = None

    def prepare_data(self, data):
        features = ['distance', 'traffic_density', 'temperature', 'is_holiday',
                    'hour', 'day_of_week', 'month', 'is_weekend']

        X = data[features]
        y = data['travel_time']

        # One-hot encode categorical variables
        X = pd.get_dummies(data[['weather_condition']], prefix=['weather'])
        X = pd.concat([data[features], X], axis=1)

        return X, y

    def train(self, data):
        X, y = self.prepare_data(data)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Model trained. MSE: {mse:.2f}, R2 Score: {r2:.2f}")

        # Calculate feature importance
        self.feature_importance = dict(
            zip(X.columns, self.model.feature_importances_))

    def predict(self, input_data):
        X, _ = self.prepare_data(input_data)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def get_feature_importance(self):
        if self.feature_importance is None:
            raise ValueError(
                "Feature importance is not available. Train the model first.")
        return self.feature_importance


# Example usage
if __name__ == "__main__":
    from data_collection import DataCollector

    collector = DataCollector()
    data = collector.generate_sample_data(days=30)

    predictor = TrafficPredictor()
    predictor.train(data)

    # Make a prediction
    sample_input = data.iloc[:10].copy()
    prediction = predictor.predict(sample_input)
    print(f"Predicted travel times: {prediction}")

    # Print feature importance
    print("\nFeature Importance:")
    for feature, importance in predictor.get_feature_importance().items():
        print(f"{feature}: {importance:.4f}")
