from auth import hash_password, verify_password
from security import create_access_token
from database import SessionLocal
from database import engine, Base
from models import User, Prediction
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dependencies import get_current_user
from logging_config import logger
from ai_engine import (
    get_primary_driver,
    get_action_plan,
    calculate_wellness_score,
    get_stars
)
from sqlalchemy import text

import models
import joblib
import numpy as np
import pandas as pd
import shap

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Stress SensAI backend initialized.")

##load models
base_models = joblib.load("models/base_models.pkl")
scaler = joblib.load("models/scaler.pkl")
meta_model = joblib.load("models/elastic.pkl")
rf_model = base_models[-1]

explainer = shap.TreeExplainer(rf_model)

db = SessionLocal()

##Schema
class StressInput(BaseModel):
    screen_time_total: float
    average_conversation_duration: float
    total_distance_km: float
    avg_dark_time: float
    app_usage: float

class SimulationInput(BaseModel):

    current_screen_time: float
    new_screen_time: float

    current_conversation: float
    new_conversation: float

    current_mobility: float
    new_mobility: float

    current_dark_time: float
    new_dark_time: float

    current_app_usage: float
    new_app_usage: float

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateProfileRequest(BaseModel):
    name: str

@app.post("/simulate")
def simulate(
    data: SimulationInput,
    user=Depends(get_current_user)
):

    current = pd.DataFrame([{

        "screen_time_total":
        data.current_screen_time,

        "average_conversation_duration":
        data.current_conversation,

        "total_distance_km":
        data.current_mobility,

        "avg_dark_time":
        data.current_dark_time,

        "app_usage":
        data.current_app_usage

    }])

    new = pd.DataFrame([{

        "screen_time_total":
        data.new_screen_time,

        "average_conversation_duration":
        data.new_conversation,

        "total_distance_km":
        data.new_mobility,

        "avg_dark_time":
        data.new_dark_time,

        "app_usage":
        data.new_app_usage

    }])

    current_scaled = scaler.transform(current)

    new_scaled = scaler.transform(new)

    current_meta = np.zeros((1, len(base_models)))

    new_meta = np.zeros((1, len(base_models)))

    for i, model in enumerate(base_models):

        current_meta[:, i] = model.predict(current_scaled)

        new_meta[:, i] = model.predict(new_scaled)

    current_prediction = round(

        float(

            meta_model.predict(current_meta)[0]

        ),

        2

    )

    new_prediction = round(

        float(

            meta_model.predict(new_meta)[0]

        ),

        2

    )

    difference = round(

        current_prediction

        -

        new_prediction,

        2

    )

    if current_prediction == 0:

        improvement = 0

    else:

        improvement = round(

            difference

            /

            current_prediction

            *

            100,

            1

        )

    return {

        "current_prediction":

        current_prediction,

        "simulated_prediction":

        new_prediction,

        "difference":

        difference,

        "improvement":

        improvement,

        "current_score":

        calculate_wellness_score(

            current_prediction

        ),

        "new_score":

        calculate_wellness_score(

            new_prediction

        )

    }

@app.post("/predict")
def predict(
    data: StressInput,
    user=Depends(get_current_user)
):

    input_data = pd.DataFrame([{

        "screen_time_total":
        data.screen_time_total,

        "average_conversation_duration":
        data.average_conversation_duration,

        "total_distance_km":
        data.total_distance_km,

        "avg_dark_time":
        data.avg_dark_time,

        "app_usage":
        data.app_usage

    }])

    X_scaled = scaler.transform(

        input_data

    )

    meta_input = np.zeros(

        (

            1,

            len(base_models)

        )

    )

    for i, model in enumerate(base_models):

        meta_input[:, i] = model.predict(

            X_scaled

        )

    prediction = round(

        float(

            meta_model.predict(

                meta_input

            )[0]

        ),

        2

    )

    if prediction < 1.5:

        risk = "Low"

    elif prediction < 3.0:

        risk = "Medium"

    else:

        risk = "High"

    record = Prediction(

        user_id=user["user_id"],

        prediction=prediction,

        risk=risk,

        screen_time=data.screen_time_total,

        conversation=data.average_conversation_duration,

        mobility=data.total_distance_km,

        dark_time=data.avg_dark_time,

        app_usage=data.app_usage

    )

    db.add(

        record

    )

    db.commit()

    logger.info(
        f"Prediction generated | User={user['user_id']} | "
        f"Stress={prediction} | Risk={risk}"
    )


# SHAP


    shap_values = explainer.shap_values(

        X_scaled

    )

    feature_names = [

        "Screen Time",

        "Conversation",

        "Mobility",

        "Dark Time",

        "App Usage"

    ]

    shap_df = pd.DataFrame({

        "Feature":

        feature_names,

        "Impact":

        shap_values[0]

    })

    shap_df["abs"] = shap_df["Impact"].abs()


# AI ENGINE


    driver = get_primary_driver(

        shap_df

    )

    action_plan = get_action_plan(

        shap_df

    )

    wellness_score = calculate_wellness_score(

        prediction

    )

    stars = get_stars(

        wellness_score

    )


# EXTRA SUMMARY


    positive = shap_df.loc[

        shap_df["Impact"] < 0

    ]

    negative = shap_df.loc[

        shap_df["Impact"] > 0

    ]

    if len(negative):

        biggest_negative = negative.sort_values(

            "Impact",

            ascending=False

        ).iloc[0]["Feature"]

    else:

        biggest_negative = None

    if len(positive):

        biggest_positive = positive.sort_values(

            "Impact"

        ).iloc[0]["Feature"]

    else:

        biggest_positive = None


# RETURN


    return {

        "prediction":

        prediction,

        "risk":

        risk,

        "wellness_score":

        wellness_score,

        "stars":

        stars,

        "primary_driver":

        driver,

        "action_plan":

        action_plan,

        "summary":{

            "highest_positive":

            biggest_negative,

            "best_habit":

            biggest_positive

        },

        "shap":{

            "features":

            feature_names,

            "impacts":

            [

                float(v)

                for v in shap_values[0]

            ]

        }

    }

@app.post("/register")
def register(
    data: RegisterRequest
):

    existing = (

        db.query(User)

        .filter(

            User.email == data.email

        )

        .first()

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Email already exists"

        )

    user = User(

        name=data.name,

        email=data.email,

        password_hash=hash_password(

            data.password

        )

    )

    db.add(user)

    db.commit()

    db.refresh(user)

    logger.info(f"User created successfully: {user.email}")

    return {

        "message":"User created successfully",

        "user":{

            "id":user.id,

            "name":user.name,

            "email":user.email

        }

    }


@app.post("/login")
def login(
    data: LoginRequest
):

    user=(

        db.query(User)

        .filter(

            User.email==data.email

        )

        .first()

    )

    if user is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )

    if not verify_password(

        data.password,

        user.password_hash

    ):
        
        logger.warning(f"Failed login attempt: {user.email}")

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )
    
    logger.info(f"User {user.id} logged in successfully")

    token=create_access_token({

        "user_id":user.id,

        "email":user.email

    })

    return{

        "access_token":token,

        "token_type":"bearer",

        "user":{

            "id":user.id,

            "name":user.name,

            "email":user.email

        }

    }


@app.get("/profile")
def get_profile(

    user=Depends(

        get_current_user

    )

):

    db_user=(

        db.query(User)

        .filter(

            User.id==user["user_id"]

        )

        .first()

    )

    if db_user is None:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )

    return{

        "id":db_user.id,

        "name":db_user.name,

        "email":db_user.email

    }


@app.put("/profile")
def update_profile(

    data:UpdateProfileRequest,

    user=Depends(

        get_current_user

    )

):

    db_user=(

        db.query(User)

        .filter(

            User.id==user["user_id"]

        )

        .first()

    )

    if db_user is None:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )

    db_user.name=data.name.strip()

    db.commit()

    db.refresh(db_user)

    return{

        "message":"Profile updated successfully",

        "profile":{

            "id":db_user.id,

            "name":db_user.name,

            "email":db_user.email

        }

    }

@app.get("/history")
def get_history(

    user=Depends(

        get_current_user

    )

):

    records=(

        db.query(Prediction)

        .filter(

            Prediction.user_id==user["user_id"]

        )

        .order_by(

            Prediction.timestamp.asc()

        )

        .all()

    )

    history=[]

    for r in records:

        history.append({

            "id":r.id,

            "timestamp":r.timestamp,

            "prediction":round(

                r.prediction,

                2

            ),

            "risk":r.risk,

            "screen_time":r.screen_time,

            "conversation":r.conversation,

            "mobility":r.mobility,

            "dark_time":r.dark_time,

            "app_usage":r.app_usage

        })

    return history


@app.get("/analytics")
def get_analytics(

    user=Depends(

        get_current_user

    )

):

    records=(

        db.query(Prediction)

        .filter(

            Prediction.user_id==user["user_id"]

        )

        .order_by(

            Prediction.timestamp

        )

        .all()

    )

    if len(records)==0:

        return{

            "current":0,

            "average":0,

            "highest":0,

            "lowest":0,

            "total_predictions":0,

            "wellness_score":100,

            "risk_distribution":{

                "Low":0,

                "Medium":0,

                "High":0

            }

        }

    predictions=[

        r.prediction

        for r in records

    ]

    latest=round(

        predictions[-1],

        2

    )

    average=round(

        sum(predictions)

        /

        len(predictions),

        2

    )

    highest=round(

        max(predictions),

        2

    )

    lowest=round(

        min(predictions),

        2

    )

    risk_distribution={

        "Low":0,

        "Medium":0,

        "High":0

    }

    for record in records:

        risk_distribution[

            record.risk

        ]+=1

    return{

        "current":latest,

        "average":average,

        "highest":highest,

        "lowest":lowest,

        "total_predictions":len(records),

        "wellness_score":

        calculate_wellness_score(

            latest

        ),

        "risk_distribution":

        risk_distribution

    }


@app.get("/dashboard-summary")
def dashboard_summary(

    user=Depends(

        get_current_user

    )

):

    analytics=get_analytics(

        user

    )

    profile=get_profile(

        user

    )

    return{

        "profile":profile,

        "analytics":analytics

    }


# OPTIONAL HEALTH CHECK ENDPOINTS


@app.get("/")
def home():

    return {

        "application":"Stress SensAI",

        "version":"2.0",

        "status":"Running",

        "authentication":"JWT",

        "database":"PostgreSQL",

        "model":"ElasticNet Stacked Ensemble"

    }


@app.get("/health")
def health():

    try:

        db.execute(text("SELECT 1"))

        database_status="Connected"

        logger.info("Database connection is healthy.")

    except Exception:

        database_status="Disconnected"

        logger.error("Database connection is failed: {e}")

    return{

        "server":"Healthy",

        "database":database_status,

        "authentication":"Working",

        "prediction_model":"Loaded"

    }



# USER STATISTICS


@app.get("/statistics")
def statistics(

    user=Depends(

        get_current_user

    )

):

    records=(

        db.query(Prediction)

        .filter(

            Prediction.user_id==user["user_id"]

        )

        .all()

    )

    if len(records)==0:

        return{

            "predictions":0,

            "low":0,

            "medium":0,

            "high":0,

            "average":0

        }

    low=sum(

        1

        for r in records

        if r.risk=="Low"

    )

    medium=sum(

        1

        for r in records

        if r.risk=="Medium"

    )

    high=sum(

        1

        for r in records

        if r.risk=="High"

    )

    average=round(

        sum(

            r.prediction

            for r in records

        )

        /

        len(records),

        2

    )

    return{

        "predictions":len(records),

        "low":low,

        "medium":medium,

        "high":high,

        "average":average

    }



# DELETE ALL HISTORY


@app.delete("/history")
def delete_history(

    user=Depends(

        get_current_user

    )

):

    (

        db.query(Prediction)

        .filter(

            Prediction.user_id==user["user_id"]

        )

        .delete()

    )

    db.commit()

    logger.info(
        f"Prediction history deleted for user {user['user_id']}"
    )

    return{

        "message":"Prediction history deleted successfully."

    }



# MODEL INFORMATION


@app.get("/model-info")
def model_information():

    return{

        "meta_model":"ElasticNet",

        "base_models":[

            "Support Vector Regressor",

            "Lasso Regression",

            "Random Forest Regressor"

        ],

        "features":[

            "Screen Time",

            "Conversation Duration",

            "Mobility",

            "Dark Time",

            "App Usage"

        ],

        "prediction_range":"0 - 5",

        "explainability":"SHAP"

    }

