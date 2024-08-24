import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class DataCollector:
    def __init__(self):
        self.data = None

    def generate_sample_data(self, days=60):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='h')

        locations = ['Store A', 'Store B', 'Warehouse X', 'Warehouse Y']

        data = []
        for dt in date_range:
            for start in locations:
                for end in locations:
                    if start != end:
                        data.append({
                            'datetime': dt,
                            'start_location': start,
                            'end_location': end,
                            'distance': np.random.uniform(50, 500),  # miles
                            'traffic_density': np.random.uniform(0, 1),
                            'weather_condition': np.random.choice(['Clear', 'Rain', 'Snow']),
                            # Fahrenheit
                            'temperature': np.random.uniform(0, 100),
                            'is_holiday': np.random.choice([0, 1], p=[0.97, 0.03]),
                            'travel_time': np.random.uniform(1, 10)  # hours
                        })

        self.data = pd.DataFrame(data)
        self.data['hour'] = self.data['datetime'].dt.hour
        self.data['day_of_week'] = self.data['datetime'].dt.dayofweek
        self.data['month'] = self.data['datetime'].dt.month
        self.data['is_weekend'] = (self.data['day_of_week'] >= 5).astype(int)

        return self.data

    def save_data_to_csv(self, filename='logistics_data.csv'):
        if self.data is not None:
            self.data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save. Generate sample data first.")

    def get_data_as_dataframe(self):
        if self.data is None:
            print("No data available. Generate sample data first.")
            return pd.DataFrame()
        return self.data


# Example usage
if __name__ == "__main__":
    collector = DataCollector()
    data = collector.generate_sample_data(days=7)
    print(data.head())
    print(f"Total records: {len(data)}")
    collector.save_data_to_csv()
