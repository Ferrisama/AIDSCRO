# src/data_collection.py

import random
from datetime import datetime, timedelta
import pandas as pd


class DataCollector:
    def __init__(self):
        self.data = []

    def generate_sample_data(self, days=30):
        """Generate sample data for a smart city over a specified number of days."""
        start_date = datetime.now() - timedelta(days=days)
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            for hour in range(24):
                timestamp = current_date + timedelta(hours=hour)
                self.data.append({
                    'timestamp': timestamp,
                    'energy_consumption': random.uniform(100, 500),  # kWh
                    'traffic_density': random.uniform(0, 1),  # 0-1 scale
                    'air_quality_index': random.randint(0, 500),  # AQI
                    'waste_generated': random.uniform(10, 100),  # tons
                    # cubic meters
                    'water_consumption': random.uniform(1000, 5000),
                })

    def get_data_as_dataframe(self):
        """Return the collected data as a pandas DataFrame."""
        return pd.DataFrame(self.data)

    def save_data_to_csv(self, filename='smart_city_data.csv'):
        """Save the collected data to a CSV file."""
        df = self.get_data_as_dataframe()
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


# Example usage
if __name__ == "__main__":
    collector = DataCollector()
    collector.generate_sample_data(days=30)
    df = collector.get_data_as_dataframe()
    print(df.head())
    collector.save_data_to_csv()
