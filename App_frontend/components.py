import streamlit as st
import pandas as pd



# TOP METRIC CARDS


def metric_cards(prediction, model, risk, color):

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(f"""
<div class="metric-card">

<h4>🧠 Predicted Stress</h4>

<h1>{prediction:.2f}</h1>

<p style="color:#6B7280;">
Current AI Prediction
</p>

</div>
""", unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
<div class="metric-card-blue">

<h4>🤖 AI Engine</h4>

<h2>{model}</h2>

<p>
Stacked Ensemble Model
</p>

</div>
""", unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
<div class="metric-card-green">

<h4>⚠️ Risk Level</h4>

<h1 style="color:{color};">

{risk}

</h1>

</div>
""", unsafe_allow_html=True)



# WELLNESS CARD


def wellness_card(score, stars):

    if score >= 80:

        status = "Excellent"

    elif score >= 60:

        status = "Healthy"

    elif score >= 40:

        status = "Needs Attention"

    else:

        status = "High Stress"

    st.markdown("""
## ❤️ Wellness Score
""")

    st.markdown(f"""
<div class="wellness-card">
<h1>
{score}/100
</h1>
<h3>
{status}
</h3>
<h2>
{stars}
</h2>
</div>

""", unsafe_allow_html=True)



# PRIMARY DRIVER


def primary_driver_card(driver):

    st.markdown("""

## 🎯 Primary Stress Driver

""")

    st.markdown(f"""
<div class="recommend-card">
<h2>
{driver["icon"]}
{driver["title"]}
</h2>

<hr>

<h3>
Contribution
</h3>

<h1>
{driver["impact"]:+.2f}
</h1>

</div>
""", unsafe_allow_html=True)



# RECOMMENDATION


def recommendation_card(driver):

    st.markdown("""
## 💡 Personalized Recommendation
""")

    st.markdown(f"""
<div class="recommend-card">
<h2>
{driver["icon"]}
{driver["title"]}
</h2>
<br>
<b>📖 Why?</b>
<p>
{driver["description"]}
</p>
<hr>
<b>✅ Suggested Action</b>
<p>
{driver["action"]}
</p>
<hr>
<b>💚 Expected Benefit</b>
<p>
{driver["benefit"]}
</p>
<hr>
<b>🔥 Motivation</b>
<p>
{driver["motivation"]}
</p>
</div>
""", unsafe_allow_html=True)



# ACTION PLAN


def action_plan(actions):

    st.markdown("""
## 🧠 Personalized Action Plan
""")
    for item in actions:

        st.markdown(f"""
<div class="action-card">
<h3>
{item["priority"]}
</h3>
<h2>
{item["icon"]}
{item["action"]}
</h2>
<hr>
<b>
⏱️ Estimated Time
</b>
<p>
{item["time"]}
</p>
<b>
🟢 Difficulty
</b>
<p>
{item["difficulty"]}
</p>
<b>
💚 Expected Benefit
</b>
<p>
{item["benefit"]}
</p>
<b>
💬 Motivation
</b>
<p>
{item["motivation"]}
</p>
<b>
📈 Estimated Improvement
</b>
<p>
{item["expected_improvement"]}
</p>
</div>
""", unsafe_allow_html=True)



# HISTORY TABLE


def history_table(history):

    if len(history) == 0:

        st.info("No Prediction History Available")

        return

    df = pd.DataFrame(history)

    def badge(risk):

        if risk == "Low":

            return "🟢 Low"

        elif risk == "Medium":

            return "🟡 Medium"

        return "🔴 High"

    df["risk"] = df["risk"].apply(badge)

    st.markdown("""

## 📋 Recent Predictions

""")

    st.dataframe(

        df.tail(5),

        use_container_width=True,

        hide_index=True

    )



# ANALYTICS CARDS


def analytics_cards(analytics):

    st.markdown("""

## 📊 Analytics Summary

""")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(

            "📍 Current",

            analytics["current"]

        )

    with c2:

        st.metric(

            "📊 Average",

            analytics["average"]

        )

    with c3:

        st.metric(

            "📈 Highest",

            analytics["highest"]

        )

    with c4:

        st.metric(

            "📉 Lowest",

            analytics["lowest"]

        )

    with c5:

        st.metric(

            "📝 Total",

            analytics["total_predictions"]

        )



# TREND CARD


def trend_card(history):

    if len(history) < 2:

        st.info(

            "Your first prediction has been recorded."

        )

        return

    df = pd.DataFrame(history)

    latest = df["prediction"].iloc[-1]

    previous = df["prediction"].iloc[-2]

    change = latest - previous

    percent = abs(change / previous * 100) if previous != 0 else 0

    st.markdown("""

## 📈 Stress Trend

""")

    if change > 0:

        st.warning(

            f"""

Stress increased by **{change:.2f}**

({percent:.1f}%)

compared to your previous prediction.

"""

        )

    elif change < 0:

        st.success(

            f"""

Stress decreased by **{abs(change):.2f}**

({percent:.1f}%)

compared to your previous prediction.

"""

        )

    else:

        st.info(

            "No significant change from the previous prediction."

        )