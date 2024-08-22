# src/resource_optimization.py

import pandas as pd
import numpy as np
from src.ai_model import SmartCityPredictor


class ResourceOptimizer:
    def __init__(self, predictor: SmartCityPredictor):
        self.predictor = predictor

    def optimize_energy_consumption(self, current_data: pd.DataFrame):
        # Predict energy consumption for the next 24 hours
        future_data = self._prepare_future_data(current_data)
        predictions = self.predictor.predict(future_data)

        # Identify peak consumption hours
        peak_hours = self._identify_peak_hours(predictions)

        # Generate optimization strategies
        strategies = self._generate_strategies(future_data, peak_hours)

        return strategies

    def _prepare_future_data(self, current_data: pd.DataFrame):
        # Prepare data for the next 24 hours based on current trends
        future_data = current_data.copy()
        for i in range(24):
            new_row = future_data.iloc[-1].copy()
            new_row['hour'] = (new_row['hour'] + 1) % 24
            new_row['is_weekend'] = 1 if new_row['day_of_week'] in [5, 6] else 0
            future_data = future_data.append(new_row, ignore_index=True)
        return future_data.tail(24)

    def _identify_peak_hours(self, predictions):
        # Identify hours with energy consumption above 75th percentile
        threshold = np.percentile(predictions, 75)
        return [i for i, pred in enumerate(predictions) if pred > threshold]

    def _generate_strategies(self, future_data, peak_hours):
        strategies = []
        feature_importance = self.predictor.get_feature_importance()
        top_features = sorted(feature_importance.items(),
                              key=lambda x: x[1], reverse=True)[:3]

        for hour in peak_hours:
            hour_data = future_data.iloc[hour]
            for feature, importance in top_features:
                if feature == 'traffic_density' and hour_data['traffic_density'] > 0.7:
                    strategies.append(f"Hour {hour}: Implement traffic reduction measures to decrease high traffic density ({
                                      hour_data['traffic_density']:.2f}).")
                elif feature == 'air_quality_index' and hour_data['air_quality_index'] > 150:
                    strategies.append(f"Hour {hour}: Activate air purification systems to improve poor air quality (AQI: {
                                      hour_data['air_quality_index']}).")
                elif feature == 'waste_generated' and hour_data['waste_generated'] > 75:
                    strategies.append(f"Hour {hour}: Optimize waste collection routes to manage high waste generation ({
                                      hour_data['waste_generated']:.2f} tons).")
                elif feature == 'water_consumption' and hour_data['water_consumption'] > 4000:
                    strategies.append(f"Hour {hour}: Implement water conservation measures to reduce high water consumption ({
                                      hour_data['water_consumption']:.2f} cubic meters).")

        return strategies


# Example usage
if __name__ == "__main__":
    predictor = SmartCityPredictor()
    predictor.train('smart_city_data.csv')
    optimizer = ResourceOptimizer(predictor)

    # Assuming we have current data
    current_data = pd.read_csv('smart_city_data.csv').tail(24)
    strategies = optimizer.optimize_energy_consumption(current_data)

    print("Optimization Strategies:")
    for strategy in strategies:
        print(strategy)
