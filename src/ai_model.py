# src/ai_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel


class SmartCityPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None

    def prepare_data(self, df):
        """Prepare the data for training and prediction."""
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

        # Create lag features
        for col in ['energy_consumption', 'traffic_density', 'air_quality_index', 'waste_generated', 'water_consumption']:
            df[f'{col}_lag_1'] = df[col].shift(1)
            df[f'{col}_lag_24'] = df[col].shift(24)

        # Select features and target
        features = ['hour', 'day_of_week', 'month', 'is_weekend', 'traffic_density', 'air_quality_index',
                    'waste_generated', 'water_consumption', 'energy_consumption_lag_1', 'energy_consumption_lag_24',
                    'traffic_density_lag_1', 'air_quality_index_lag_1', 'waste_generated_lag_1', 'water_consumption_lag_1']
        target = 'energy_consumption'

        X = df[features]
        y = df[target]

        return X, y

    def train(self, data_file):
        """Train the model on the provided data."""
        df = pd.read_csv(data_file)
        X, y = self.prepare_data(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Create a pipeline with imputation, scaling, feature selection, and the model
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler()),
            ('feature_selection', SelectFromModel(
                RandomForestRegressor(n_estimators=100, random_state=42))),
            ('regressor', RandomForestRegressor(random_state=42))
        ])

        # Define hyperparameters for grid search
        param_grid = {
            'regressor__n_estimators': [100, 200, 300],
            'regressor__max_depth': [10, 20, 30, None],
            'regressor__min_samples_split': [2, 5, 10],
            'regressor__min_samples_leaf': [1, 2, 4]
        }

        # Perform grid search
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_

        # Make predictions on the test set
        y_pred = self.model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Model trained. MSE: {mse:.2f}, R2 Score: {r2:.2f}")
        print(f"Best parameters: {grid_search.best_params_}")

        # Calculate feature importance
        feature_importance = self.model.named_steps['regressor'].feature_importances_
        feature_names = self.model.named_steps['feature_selection'].get_feature_names_out(
            X.columns)
        self.feature_importance = dict(zip(feature_names, feature_importance))

        print("Top 5 important features:")
        for feature, importance in sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"{feature}: {importance:.4f}")

    def predict(self, input_data):
        """Make predictions using the trained model."""
        if self.model is None:
            raise ValueError(
                "Model has not been trained yet. Call train() first.")
        return self.model.predict(input_data)

    def get_feature_importance(self):
        """Return the feature importance if the model has been trained."""
        if self.feature_importance is None:
            raise ValueError(
                "Feature importance is not available. Train the model first.")
        return self.feature_importance


# Example usage
if __name__ == "__main__":
    predictor = SmartCityPredictor()
    predictor.train('smart_city_data.csv')

    # Example prediction
    sample_input = pd.DataFrame({
        'hour': [12],
        'day_of_week': [2],
        'month': [6],
        'is_weekend': [0],
        'traffic_density': [0.5],
        'air_quality_index': [100],
        'waste_generated': [50],
        'water_consumption': [3000],
        'energy_consumption_lag_1': [250],
        'energy_consumption_lag_24': [260],
        'traffic_density_lag_1': [0.48],
        'air_quality_index_lag_1': [98],
        'waste_generated_lag_1': [48],
        'water_consumption_lag_1': [2950]
    })
    prediction = predictor.predict(sample_input)
    print(f"Predicted energy consumption: {prediction[0]:.2f} kWh")

    print("\nFeature Importance:")
    for feature, importance in predictor.get_feature_importance().items():
        print(f"{feature}: {importance:.4f}")
