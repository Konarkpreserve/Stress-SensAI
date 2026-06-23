import requests
import json
import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor



# PAGE CONFIG
st.set_page_config(
    page_title="Interpretable Stacked Ensemble for Personlized Stress Prediction",
    layout="wide",
    page_icon="🧠"
)


# 🎨 CALM UI THEME (SAGE + BLUE)

st.markdown("""
<style>

/* Background */
.main {
    background-color: #f5f7f6;
}

/* Text */
h1, h2, h3, p {
    color: #1f2937;
}

/* Cards */
.metric-card {
    padding: 20px;
    border-radius: 16px;
    background-color: #e6f4ea;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    h1, h2, h3, p {
        color: #000000;
        }
}

.metric-card-blue {
    padding: 20px;
    border-radius: 16px;
    background-color: #e0f2fe;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    h1, h2, h3, p {
        color: #000000;
        }
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #60a5fa, #86efac);
    color: #1f2937;
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
    border: none;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ecfdf5;
    h1, h2, h3, p {
            color: #000000;
            }
}
            
/* dropdown going behind */
div[data-baseweb="select"] {
    z-index: 9999 !important;
}

/* popover */
div[data-baseweb="popover"] {
    z-index: 9999 !important;
}
        
/* Sidebar dropdown fix */
section[data-testid="stSidebar"] {
    z-index: 10000 !important;
}

/* Ensure sidebar content stays above */
section[data-testid="stSidebar"] * {
    z-index: 10000 !important;
}

</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown("""
# 🧠 Interpretable Stacked Ensemble for Personlized Stress Prediction
### Personalized Stress Intelligence Platform
""")

st.caption("Calm UI • Explainable AI • Personalized Insights")


# SIDEBAR

st.sidebar.title("⚙️ Controls")

input_type = st.sidebar.radio(
    "Input Method",
    ["Manual Input (3 Days)", "Upload CSV"]
)


# MODELS

def get_base_models():
    return [
        SVR(kernel="linear"),
        Lasso(alpha=0.1),
        RandomForestRegressor(n_estimators=100)
    ]


# INPUT SECTION

st.markdown("## 📥 Behavioral Input (3-Day Average)")

if input_type == "Manual Input (3 Days)":

    def input_3day(feature, unit=""):

        c1, c2, c3 = st.columns(3)

        with c1:
            d1 = st.number_input(
                f"{feature} - Day 1 {unit}",
                min_value=0.0,
                value=None,
                placeholder="Enter value",
                key=feature+"1"
            )

        with c2:
            d2 = st.number_input(
                f"{feature} - Day 2 {unit}",
                min_value=0.0,
                value=None,
                placeholder="Enter value",
                key=feature+"2"
            )

        with c3:
            d3 = st.number_input(
                f"{feature} - Day 3 {unit}",
                min_value=0.0,
                value=None,
                placeholder="Enter value",
                key=feature+"3"
            )

        values = [d1, d2, d3]

        # replace None with 0 safely
        values = [0 if v is None else v for v in values]

        return sum(values) / 3
    
    screen = input_3day("Screen Time", "(minutes)")
    conv = input_3day("Conversation", "(minutes)")
    mobility = input_3day("Mobility", "(km)")
    dark = input_3day("Dark Time", "(hours)")
    app_usage = input_3day("App Usage", "(minutes)")

    input_data = pd.DataFrame([[
        screen,
        conv,
        mobility,
        dark,
        app_usage
    ]], columns=[
        "screen_time_total",
        "average_conversation_duration",
        "total_distance_km",
        "avg_dark_time",
        "app_usage"
    ])

    # screen = input_3day("Screen Time")
    # conv = input_3day("Conversation")
    # mobility = input_3day("Mobility")
    # sleep = input_3day("Sleep")
    # dark = input_3day("Dark Time")

    # Baseline from 3-day data
    # baseline = np.mean([screen, conv, mobility, sleep, dark])

    # input_data = pd.DataFrame([[screen, conv, mobility, sleep, dark]])

else:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file:
        input_data = pd.read_csv(uploaded_file)

        # Ensure required columns exist
        required_cols = [
            "screen_time_total",
            "average_conversation_duration",
            "total_distance_km",
            "avg_dark_time",
            "app_usage"
        ]

        input_data = input_data[required_cols]

    else:
        input_data = None
        stress_avg = None


# PREDICTION

if st.button("🚀 Analyze Stress", use_container_width=True):

    if input_data is None:
        st.warning("Please provide input data")
    else:
        


        payload = {
            "screen_time_total": float(screen),
            "average_conversation_duration": float(conv),
            "total_distance_km": float(mobility),
            "avg_dark_time": float(dark),
            "app_usage": float(app_usage)
        }

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        result = response.json()

        pred = result["prediction"]
        risk = result["risk"]
        
        if risk == "Low":
            color = "#22c55e"
        elif risk == "Medium":
            color = "#eab308"
        else:
            color = "#ef4444"

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "prediction": float(pred),
            "screen_time": float(screen),
            "conversation": float(conv),
            "mobility": float(mobility),
            "dark_time": float(dark),
            "app_usage": float(app_usage)
        }

        history_file = "history.json"

        if os.path.exists(history_file):

            with open(history_file, "r") as f:
                history =json.load(f)
        else:
            history = []
            
        history.append(record)

        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)




        
        # OUTPUT
        
        st.markdown("## 📊 Insights")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
            <h4>Predicted Stress</h4>
            <h2>{pred:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card-blue">
            <h4>AI engine</h4>
            <h2>ElasticNet Ensemble</h2>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
            <h4>Risk Level</h4>
            <h2 style="color:{color}">{risk}</h2>
            </div>
            """, unsafe_allow_html=True)

        
        # VISUAL
        
        st.markdown("## 📈 Stress Bar")

        chart = pd.DataFrame({
            "Metric": ["Predicted Stress"],
            "Value": [pred]
        })

        st.bar_chart(chart.set_index("Metric"))

        
        # EXPLANATION
        
        st.markdown("## 🧠 AI Insights")

        try:
            # Fix input shape
            X_input = np.array(X_input).reshape(1, -1)

            rf_model = base_models[-1]

            explainer = shap.TreeExplainer(rf_model)
            shap_values = explainer.shap_values(X_input)

            feature_names = [
                "Screen Time",
                "Conversation",
                "Mobility",
                "Dark Time",
                "App Usage"
            ]

            shap_df = pd.DataFrame({
                "Feature": feature_names,
                "Impact": shap_values[0]
            })

            shap_df["abs"] = shap_df["Impact"].abs()
            shap_df = shap_df.sort_values("abs", ascending=True)

            # Plot
            fig, ax = plt.subplots()
            ax.barh(shap_df["Feature"], shap_df["Impact"])
            ax.set_title("Feature Contribution to Stress")
            ax.set_xlabel("Impact")

            st.pyplot(fig)

            # Text explanation
            st.markdown("### 🧠 Personalized Insights")

            top = shap_df.sort_values("abs", ascending=False).head(3)

            for _, row in top.iterrows():

                feature = row["Feature"]
                impact = row["Impact"]

                if feature == "Screen Time":

                    if impact > 0:
                        st.info(
                            "Higher screen usage appears to be contributing to elevated stress levels."
                        )
                    else:
                        st.success(
                            "Screen usage patterns appear healthy and are helping reduce stress."
                        )

                elif feature == "Mobility":

                    if impact > 0:
                        st.info(
                            "Lower physical activity may be contributing to increased stress."
                        )
                    else:
                        st.success(
                            "Regular movement and mobility are helping maintain lower stress."
                        )

                elif feature == "Dark Time":

                    if impact > 0:
                        st.info(
                            "Rest and inactivity patterns may be influencing stress levels."
                        )
                    else:
                        st.success(
                            "Healthy rest patterns appear beneficial for stress management."
                        )

                elif feature == "Conversation":

                    st.info(
                        "Social interaction patterns played an important role in this prediction."
                    )

                elif feature == "App Usage":

                    if impact > 0:
                        st.info(
                            "Extended application usage may be contributing to increased stress."
                        )
                    else:
                        st.success(
                            "Application usage appears balanced and supportive of wellbeing."
                        )
            

        except Exception as e:
            st.error(f"SHAP ERROR: {e}")

        st.markdown("Stress Trend")

        if os.path.exists("history.json"):

            with open("history.json", "r") as f:
                history = json.load(f)

            if len(history) > 0:

                history_df = pd.DataFrame(history)

                st.line_chart(
                    history_df.set_index("timestamp")["prediction"]
                )

# ANALYTICS SUMMARY

        avg_stress = history_df["prediction"].mean()
        max_stress = history_df["prediction"].max()
        min_stress = history_df["prediction"].min()
        latest = history_df["prediction"].iloc[-1]

        st.markdown("### 📈📉Analytics Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Current", f"{latest:.2f}")

        with c2:
            st.metric("Average", f"{avg_stress:.2f}")

        with c3:
            st.metric("Highest", f"{max_stress:.2f}")

        with c4:
            st.metric("Lowest", f"{min_stress:.2f}")
        
# TREND DETECTION

        if len(history_df) >= 2:

            previous = history_df["prediction"].iloc[-2]

            change = latest - previous

            if change > 0:
                st.warning(
                    f"Stress increased by {change:.2f} compared to your previous entry."
                )

            elif change < 0:
                st.success(
                    f"Stress decreased by {abs(change):.2f} compared to your previous entry."
                )

            else:
                st.info(
                    "Stress level remained stable."
                )
                
        st.success("Analysis complete ✔")

        st.download_button(...)