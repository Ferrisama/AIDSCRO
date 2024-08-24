from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

from src.data_collection import DataCollector
from src.ai_model import TrafficPredictor
from src.visualization import plot_feature_importance, plot_traffic_prediction, create_html_report


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the React app
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

data_collector = DataCollector()
predictor = TrafficPredictor()


class PredictionInput(BaseModel):
    start_location: str
    end_location: str
    distance: float
    traffic_density: float
    weather_condition: str
    temperature: float
    is_holiday: int
    hour: int
    day_of_week: int
    month: int
    is_weekend: int


@app.on_event("startup")
async def startup_event():
    data = data_collector.generate_sample_data(days=60)
    data_collector.save_data_to_csv('logistics_data.csv')
    predictor.train(data)


@app.get("/")
async def root():
    return {"message": "Welcome to AIDSCRO - Traffic Prediction System"}


@app.get("/data")
async def get_data():
    df = data_collector.get_data_as_dataframe()
    # Return only first 100 records for brevity
    return df.head(100).to_dict(orient='records')


@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        input_df = pd.DataFrame([input_data.dict()])
        prediction = predictor.predict(input_df)
        return {"predicted_travel_time": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/feature_importance")
async def get_feature_importance():
    try:
        return predictor.get_feature_importance()
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
        prediction_plot = plot_traffic_prediction(y, predictions)

        html_report = create_html_report(
            feature_importance_plot, prediction_plot, [])
        return HTMLResponse(content=html_report, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
