
import streamlit as st
import pandas as pd
from datetime import datetime

from styles import load_css

from auth import (
    require_login,
    get_token,
    logout_button
)

from api import (
    get_profile,
    update_profile,
    predict,
    get_history,
    get_analytics
)

from components import (
    metric_cards,
    wellness_card,
    primary_driver_card,
    recommendation_card,
    action_plan,
    history_table,
    analytics_cards,
    trend_card
)

from charts import (
    stress_bar,
    shap_chart,
    shap_insights,
    stress_trend,
    wellness_progress
)

from simulator import (
    habit_optimizer
)

from report import (
    create_report
)

from utils import (
    create_prediction_payload,
    get_risk_color,
    greeting
)


# PAGE CONFIG


st.set_page_config(

    page_title="Stress SensAI",

    page_icon="🧠",

    layout="wide"

)

st.markdown(

    load_css(),

    unsafe_allow_html=True

)


# LOGIN


require_login()

token = get_token()


# SESSION STATE


if "analysis" not in st.session_state:
    st.session_state["analysis"] = None


# PROFILE


try:
    profile = get_profile(token).json()
    analytics = get_analytics(token).json()
except Exception:
    st.error("Unable to connect to the backend.")
    st.stop()


# HEADER


hour = datetime.now().hour

today = datetime.now().strftime("%d %B %Y")

st.markdown(f"""
<div class="hero-card">

<h1 style="margin-bottom:5px;color:white;">

{greeting(hour)}, {profile["name"]} 👋

</h1>

<h3 style="color:white;font-weight:400;">

Welcome back to <b>Stress SensAI</b>

</h3>

<p style="font-size:17px;color:white;opacity:.95;">

🗓️ {today}

<br>

AI Powered Personalized Stress Intelligence Platform

</p>

</div>
""", unsafe_allow_html=True)

st.markdown(
"""
### 🌿 Your Personal Wellness Dashboard

Monitor your stress, understand the contributing factors,
and receive AI-powered recommendations to improve your wellbeing.
"""
)
st.caption(

f"Last Analysis: {datetime.now().strftime('%d %B %Y • %I:%M %p')}"

)



# SIDEBAR


st.sidebar.markdown(
f"""
<div style="
    background:white;
    padding:22px;
    border-radius:20px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:20px;
    text-align:center;
">

<div style="font-size:55px;">
👤
</div>

<h2 style="margin-bottom:0;">

{profile["name"]}

</h2>

<p style="
color:#6B7280;
font-size:15px;
">

{profile["email"]}

</p>

<hr>

</div>

""",

unsafe_allow_html=True

)


# ACCOUNT SUMMARY


st.sidebar.markdown("### 📊 Account Summary")

col1,col2 = st.sidebar.columns(2)

with col1:

    st.metric(

        "Predictions",

        analytics["total_predictions"]

    )

with col2:

    st.metric(
        "Wellness",
        analytics["current"]

    )

st.sidebar.markdown("---")


# PROFILE UPDATE


st.sidebar.markdown("### ✏️ Update Profile")

new_name = st.sidebar.text_input(

    "Display Name",

    value=profile["name"],

    placeholder="Enter new name"

)

if st.sidebar.button(

    "💾 Save Changes",

    use_container_width=True

):

    response = update_profile(

        token,

        new_name

    )

    if response.status_code == 200:

        st.sidebar.success(

            "Profile Updated Successfully"

        )

        st.rerun()

st.sidebar.markdown("---")


# INPUT METHOD


st.sidebar.markdown("### ⚙️ Input Method")

input_type = st.sidebar.radio(

    "Input Method",

    [
        "Manual Input (3 Days)",
        "Upload CSV"
    ],
    label_visibility="collapsed"

)

st.sidebar.markdown("---")

logout_button()

# INPUT TITLE


st.markdown(
"""
<div style = "background:white; padding:25px;
border-radius:22px;
box-shadow:0 8px 20px rgba(0,0,0,.08);
margin-bottom:20px;
">


<h2>

📥 Behavioral Inputs

</h2>

<p style="color:#6B7280;">
Enter your average behavioural data from the last 3 days.
These values help the AI generate more stable and accurate predictions.
</p>

</div>

""",

unsafe_allow_html=True
)


# INPUT SECTION


payload = None

screen = 0.0
conversation = 0.0
mobility = 0.0
dark = 0.0
app_usage = 0.0


# MANUAL INPUT


if input_type == "Manual Input (3 Days)":

    def average_input(

        feature,

        unit,

        key

    ):

        c1, c2, c3 = st.columns(3)

        with c1:

            d1 = st.number_input(

                f"{feature} Day 1 {unit}",

                min_value=0.0,

                value=None,

                placeholder="Enter Value",

                key=f"{key}_1"

            )

        with c2:

            d2 = st.number_input(

                f"{feature} Day 2 {unit}",

                min_value=0.0,

                value=None,

                placeholder="Enter Value",

                key=f"{key}_2"

            )

        with c3:

            d3 = st.number_input(

                f"{feature} Day 3 {unit}",

                min_value=0.0,

                value=None,

                placeholder="Enter Value",

                key=f"{key}_3"

            )

        values = [d1, d2, d3]
        values = [0 if v is None else v for v in values]

        return round(sum(values) / 3, 2)

    screen = average_input(

        "Screen Time",

        "(minutes)",

        "screen"

    )

    conversation = average_input(

        "Conversation",

        "(minutes)",

        "conversation"

    )

    mobility = average_input(

        "Mobility",

        "(km)",

        "mobility"

    )

    dark = average_input(

        "Dark Time",

        "(hours)",

        "dark"

    )

    app_usage = average_input(

        "App Usage",

        "(minutes)",

        "app"

    )

    payload = create_prediction_payload(

        screen,

        conversation,

        mobility,

        dark,

        app_usage

    )


# CSV INPUT


else:

    uploaded_file = st.file_uploader(

        "Upload CSV",

        type=["csv"]

    )

    if uploaded_file is not None:

        df = pd.read_csv(

            uploaded_file

        )

        required = [

            "screen_time_total",

            "average_conversation_duration",

            "total_distance_km",

            "avg_dark_time",

            "app_usage"

        ]

        missing = [

            col

            for col in required

            if col not in df.columns

        ]

        if len(missing):

            st.error(

                f"Missing Columns : {missing}"

            )

            st.stop()

        row = df.iloc[0]

        screen = float(

            row["screen_time_total"]

        )

        conversation = float(

            row["average_conversation_duration"]

        )

        mobility = float(

            row["total_distance_km"]

        )

        dark = float(

            row["avg_dark_time"]

        )

        app_usage = float(

            row["app_usage"]

        )

        payload = create_prediction_payload(

            screen,

            conversation,

            mobility,

            dark,

            app_usage

        )

        st.success(

            "CSV Loaded Successfully"

        )


# ANALYZE BUTTON


st.markdown("<br>",unsafe_allow_html=True)

analyze = st.button(

    "🚀 Analyze Stress",

    use_container_width=True

)

if analyze:

    if payload is None:

        st.warning(

            "Please provide valid input."

        )

        st.stop()

    with st.spinner("🧠 AI is analyzing your behavioural patterns..."):

        response = predict(

            token,

            payload

        )


    if response.status_code != 200:

        st.error(
        """
        Prediction failed.

        Please verify:

        • Backend server is running

        • Model files exist

        • You are logged in

        • Input values are valid
        """
        )

        st.stop()

    result = response.json()

    st.session_state["analysis"] = result

    prediction = result["prediction"]

    risk = result["risk"]

    score = result["wellness_score"]

    stars = result["stars"]

    driver = result["primary_driver"]

    actions = result["action_plan"]

    shap_data = result["shap"]

    color = get_risk_color(

        risk

    )

    history = get_history(

        token

    ).json()

    analytics = get_analytics(

        token

    ).json()


# LOAD LAST ANALYSIS


if st.session_state["analysis"] is not None:

    result = st.session_state["analysis"]

    prediction = result["prediction"]

    risk = result["risk"]

    score = result["wellness_score"]

    stars = result["stars"]

    driver = result["primary_driver"]

    actions = result["action_plan"]

    shap_data = result["shap"]

    color = get_risk_color(risk)

    history = get_history(token).json()

    analytics = get_analytics(token).json()



# RESULTS DASHBOARD


    st.markdown("---")

    st.markdown("# 📊 AI Stress Analysis")

    # -----------------------------------------------------

    left,right = st.columns([1,1])

    with left:

        metric_cards(

            prediction,

            "ElasticNet Stacked Ensemble",

            risk,

            color

        )

    with right:

        wellness_card(
            score,
            stars
        )

        wellness_progress(
            score
        )

    # -----------------------------------------------------

    st.markdown("<br>",unsafe_allow_html=True)

    left,right = st.columns([1,1])

    with left:

        primary_driver_card(

            driver

        )

    with right:

        recommendation_card(

            driver

        )

    # -----------------------------------------------------

    st.markdown("<br>",unsafe_allow_html=True)

    action_plan(

        actions

    )

    # -----------------------------------------------------

    st.markdown("<br>",unsafe_allow_html=True)

    stress_bar(

        prediction

    )



# AI EXPLAINABILITY


    st.markdown("---")

    st.markdown("# 🧠 AI Explainability & Analytics")

    
    # ROW 1
    

    left,right = st.columns([1.2,1])

    with left:

        shap_df = shap_chart(

            shap_data

        )

    with right:

        shap_insights(

            shap_df

        )

    
    # ROW 2
    

    st.markdown("<br>",unsafe_allow_html=True)

    left,right = st.columns([1,1])

    if analytics["total_predictions"] == 0:
        
        st.info(
            """
    📊 Analytics will appear after your first prediction.
    """
        )

    else:

        with left:
#analytics summary
            analytics_cards(

                analytics

            )

        with right:
#stress trend
            trend_card(

                history

            )

    
    # ROW 3
    

    st.markdown("<br>",unsafe_allow_html=True)

    #recent prediction

    if len(history) == 0:

        st.info(
            """
    📝 No prediction history available yet.

    Run your first stress analysis to begin tracking your progress.
    """
        )

    else:

        history_table(
            history[-5:][::-1]
        )

        stress_trend(
            history
        )


# HABIT OPTIMIZER


    habit_optimizer(

        token,

        screen,

        conversation,

        mobility,

        dark,

        app_usage

    )



# EXPORT CENTER


    st.markdown("---")

    st.markdown("# 📥 Export Center")

    st.caption(
        "Download your complete stress analysis."
    )

    pdf = create_report(

        prediction=prediction,

        risk=risk,

        wellness_score=score,

        driver=driver,

        analytics=analytics

    )

    left,right = st.columns(2)

    with left:

        st.markdown(
            "### 📄 PDF Report"
        )

        st.caption(
            "Prediction, wellness, analytics and recommendations."
        )

        with open(pdf,"rb") as file:

            st.download_button(

                "⬇ Download PDF",

                file,

                file_name="Stress_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )

    with right:

        st.markdown(
            "### 📊 CSV History"
        )

        st.caption(
            "Complete prediction history."
        )

        history_df = pd.DataFrame(history)

        csv = history_df.to_csv(

            index=False

        ).encode(

            "utf-8"

        )

        st.download_button(

            "⬇ Download CSV",

            csv,

            file_name="Stress_History.csv",

            mime="text/csv",

            use_container_width=True

        )


# FOOTER


    st.markdown("---")

    st.markdown("""

    <div style="
    background:white;
    padding:28px;
    border-radius:20px;
    box-shadow:0 8px 20px rgba(0,0,0,.06);
    text-align:center;
    ">

    <h2>
    🧠 Stress SensAI
    </h2>

    <p style="color:#6B7280;">
    AI Powered Personalized Stress Intelligence Platform
    </p>

    <hr>

    <p>
    Built with
    <b>
    FastAPI&nbsp;&nbsp;•&nbsp;&nbsp;
    PostgreSQL&nbsp;&nbsp;•&nbsp;&nbsp;
    Streamlit&nbsp;&nbsp;•&nbsp;&nbsp;
    ElasticNet&nbsp;&nbsp;•&nbsp;&nbsp;
    JWT Authentication
    </b>
    </p>

    <p style="color:#9CA3AF;">
    Version 2.0
    </p>

    </div>

    """, unsafe_allow_html=True)