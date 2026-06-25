import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# STRESS BAR


def stress_bar(prediction):

    st.markdown("## 📈 Stress Prediction")

    chart = pd.DataFrame({

        "Metric": ["Predicted Stress"],

        "Value": [prediction]

    })

    st.bar_chart(

        chart.set_index("Metric"),

        use_container_width=True

    )



# SHAP FEATURE CONTRIBUTION


def shap_chart(shap_data):

    st.markdown("## 🧠 Feature Contribution")

    shap_df = pd.DataFrame({

        "Feature": shap_data["features"],

        "Impact": shap_data["impacts"]

    })

    shap_df["abs"] = shap_df["Impact"].abs()

    shap_df = shap_df.sort_values(

        "abs",

        ascending=True

    )

    fig, ax = plt.subplots(

        figsize=(10,5)

    )

    colors = []

    for impact in shap_df["Impact"]:

        if impact >= 0:

            colors.append("#EF4444")

        else:

            colors.append("#22C55E")

    bars = ax.barh(

        shap_df["Feature"],

        shap_df["Impact"],

        color=colors,

        height=0.55

    )

    ax.set_xlabel(

        "SHAP Impact",

        fontsize=11

    )

    ax.set_ylabel(

        ""

    )

    ax.set_title(

        "Feature Contribution",

        fontsize=15,

        fontweight="bold"

    )

    ax.grid(

        axis="x",

        linestyle="--",

        alpha=.3

    )

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_visible(False)

    for bar in bars:

        width = bar.get_width()

        ax.text(

            width,

            bar.get_y()+bar.get_height()/2,

            f"{width:.2f}",

            va="center",

            fontsize=10

        )

    st.pyplot(

        fig,

        use_container_width=True

    )

    return shap_df



# TOP FEATURE INSIGHTS


def shap_insights(shap_df):

    st.markdown("## 💡 AI Insights")

    top = shap_df.sort_values(

        "abs",

        ascending=False

    ).head(3)

    for _, row in top.iterrows():

        if row["Impact"] > 0:

            st.info(

                f"""

**{row['Feature']}**

increased your predicted stress by

**{abs(row['Impact']):.2f}**

"""

            )

        else:

            st.success(

                f"""

**{row['Feature']}**

helped reduce your stress by

**{abs(row['Impact']):.2f}**

"""

            )



# STRESS TREND


def stress_trend(history):

    if len(history) == 0:

        return

    df = pd.DataFrame(history)

    st.markdown("## 📈 Stress Trend")

    fig, ax = plt.subplots(

        figsize=(8,4)

    )

    ax.plot(

        df["timestamp"],

        df["prediction"],

        linewidth=3,

        marker="o",

        markersize=7,

        color="#3B82F6"

    )

    ax.fill_between(

        df["timestamp"],

        df["prediction"],

        alpha=.15,

        color="#93C5FD"

    )

    ax.grid(

        alpha=.25

    )

    ax.set_xlabel("")

    ax.set_ylabel("Stress")

    ax.set_title(

        "Prediction History"
    )

    plt.xticks(

        rotation=20

    )

    st.pyplot(

        fig,

        use_container_width=True

    )



# WELLNESS PROGRESS


def wellness_progress(score):

    st.markdown("### ❤️ Wellness Progress")

    st.progress(
        score/100
    )

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.metric(

            "0",

            "Poor"

        )

    with c2:

        st.metric(

            "40",

            "Fair"

        )

    with c3:

        st.metric(

            "70",

            "Healthy"

        )

    with c4:

        st.metric(

            "100",

            "Excellent"

        )

    if score>=80:

        st.success(

            "Excellent wellness. Keep maintaining your current habits."

        )

    elif score>=60:

        st.info(

            "Good wellness. A few improvements can make it even better."

        )

    elif score>=40:

        st.warning(

            "Moderate wellness. Consider following the recommendations."

        )

    else:

        st.error(

            "High stress detected. Prioritize your recommended action plan."

        )



# SIMULATION COMPARISON


def comparison_chart(

    current,

    simulated

):

    st.markdown(

        "## 🧪 What-If Simulation"

    )

    comparison = pd.DataFrame({

        "Scenario":[

            "Current",

            "Simulated"

        ],

        "Stress":[

            current,

            simulated

        ]

    })

    st.bar_chart(

        comparison.set_index(

            "Scenario"

        ),

        use_container_width=True

    )