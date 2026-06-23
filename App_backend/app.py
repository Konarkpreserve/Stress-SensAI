from database import SessionLocal
from models import Prediction
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
##load models
base_models = joblib.load("models/base_models.pkl")
scaler = joblib.load("models/scaler.pkl")
meta_model = joblib.load("models/elastic.pkl")

db = SessionLocal()

##Schema
class StressInput(BaseModel):
    screen_time_total: float
    average_conversation_duration: float
    total_distance_km: float
    avg_dark_time: float
    app_usage: float

@app.post("/predict")
def predict(data: StressInput):

    input_data = np.array([[
        data.screen_time_total,
        data.average_conversation_duration,
        data.total_distance_km,
        data.avg_dark_time,
        data.app_usage
    ]])

    X_scaled = scaler.transform(input_data)

    meta_input = np.zeros((1, len(base_models)))

    for i, model in enumerate(base_models):
        meta_input[:, i] = model.predict(X_scaled)

    prediction = round(float(
        meta_model.predict(meta_input)[0]
    ),2)

    if prediction < 1.5:
        risk = "Low"

    elif prediction < 3.0:
        risk = "Medium"

    else:
        risk = "High"

    record = Prediction(
        prediction=prediction,
        risk=risk,
        screen_time=data.screen_time_total,
        conversation=data.average_conversation_duration,
        mobility=data.total_distance_km,
        dark_time=data.avg_dark_time,
        app_usage=data.app_usage
    )

    db.add(record)
    db.commit()

    return {
        "prediction": prediction,
        "risk": risk
    }