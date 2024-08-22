# src/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

from src.data_collection import DataCollector
from src.ai_model import SmartCityPredictor
from src.visualization import plot_feature_importance, plot_energy_consumption_prediction, create_html_report
from src.resource_optimization import ResourceOptimizer

app = FastAPI()

data_collector = DataCollector()
predictor = SmartCityPredictor()
optimizer = ResourceOptimizer(predictor)


class PredictionInput(BaseModel):
    hour: int
    day_of_week: int
    month: int
    is_weekend: int
    traffic_density: float
    air_quality_index: int
    waste_generated: float
    water_consumption: float
    energy_consumption: float
    energy_consumption_lag_1: float
    energy_consumption_lag_24: float
    traffic_density_lag_1: float
    air_quality_index_lag_1: int
    waste_generated_lag_1: float
    water_consumption_lag_1: float
    energy_consumption_rolling_mean_24: float
    traffic_air_quality: float
    energy_water_interaction: float


@app.on_event("startup")
async def startup_event():
    data_collector.generate_sample_data(days=60)
    data_collector.save_data_to_csv()
    predictor.train('smart_city_data.csv')


@app.get("/")
async def root():
    return {"message": "Welcome to AIDSCRO API"}


@app.get("/data")
async def get_data():
    df = data_collector.get_data_as_dataframe()
    return df.to_dict(orient='records')


@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        input_df = pd.DataFrame([input_data.dict()])
        prediction = predictor.predict(input_df)
        return {"predicted_energy_consumption": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/feature_importance")
async def get_feature_importance():
    try:
        return predictor.get_feature_importance()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/optimize")
async def get_optimization_strategies():
    try:
        df = data_collector.get_data_as_dataframe()
        strategies = optimizer.optimize_energy_consumption(df)
        return {"optimization_strategies": strategies}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/report", response_class=HTMLResponse)
async def get_report():
    try:
        feature_importance = predictor.get_feature_importance()
        feature_importance_plot = plot_feature_importance(feature_importance)

        df = data_collector.get_data_as_dataframe()
        X, y = predictor.prepare_data(df)
        predictions = predictor.predict(X)
        prediction_plot = plot_energy_consumption_prediction(y, predictions)

        strategies = optimizer.optimize_energy_consumption(df)

        html_report = create_html_report(
            feature_importance_plot, prediction_plot, strategies)
        return HTMLResponse(content=html_report, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
