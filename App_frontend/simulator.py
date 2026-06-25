
import streamlit as st

from api import simulate

from utils import (
    FEATURES,
    SLIDER_LIMITS,
    current_values,
    get_feature_value,
    create_simulation_payload
)

from charts import comparison_chart



# HABIT OPTIMIZER


def habit_optimizer(

    token,

    screen,
    conversation,
    mobility,
    dark,
    app_usage

):

    st.markdown("---")

    st.markdown("""
# 🧪 AI Habit Optimizer

Improve one habit and instantly see
how your predicted stress changes.
""")

    values = current_values(

        screen,

        conversation,

        mobility,

        dark,

        app_usage

    )


# FEATURE SELECTION


    col1, col2 = st.columns([2,1])

    with col1:

        feature = st.selectbox(

            "Lifestyle Habit",

            FEATURES

        )

    current = get_feature_value(

        feature,

        values

    )

    minimum, maximum = SLIDER_LIMITS[feature]

    with col2:

        st.metric(

            "Current",

            round(current,2)

        )


# SLIDER


    target = st.slider(

        f"Target {feature}",

        min_value=float(minimum),

        max_value=float(maximum),

        value=float(current),

        step=1.0

    )


# INFO


    if feature == "Screen Time":

        st.info(

            "📱 Lower screen time generally reduces digital fatigue and mental stress."

        )

    elif feature == "Conversation":

        st.info(

            "💬 Healthy conversations often improve emotional well-being."

        )

    elif feature == "Mobility":

        st.info(

            "🚶 Regular walking and physical activity can significantly lower stress."

        )

    elif feature == "Dark Time":

        st.info(

            "🌙 Maintaining healthy night-time routines improves recovery."

        )

    else:

        st.info(

            "📲 Reducing excessive app usage improves focus and mental health."

        )


# BUTTON


    if st.button(

        "🚀 Run AI Simulation",

        use_container_width=True

    ):

        payload = create_simulation_payload(

            feature,

            values,

            target

        )

        response = simulate(

            token,

            payload

        )

        if response.status_code != 200:

            st.error(

                "Simulation failed."

            )

            return

        result = response.json()


# RESULTS


        st.markdown("---")

        st.markdown("# 📊 Simulation Result")

        a,b,c = st.columns(3)

        with a:

            st.metric(

                "Current Stress",

                round(

                    result["current_prediction"],

                    2

                )

            )

        with b:

            st.metric(

                "Simulated Stress",

                round(

                    result["simulated_prediction"],

                    2

                ),

                delta=round(

                    result["difference"],

                    2

                )

            )

        with c:

            st.metric(

                "Improvement",

                f'{result["improvement"]:.1f}%'

            )


# WELLNESS


        st.markdown("## ❤️ Wellness Improvement")

        x,y = st.columns(2)

        with x:

            st.metric(

                "Current Score",

                result["current_score"]

            )

        with y:

            st.metric(

                "New Score",

                result["new_score"],

                delta=result["new_score"]-result["current_score"]

            )

        st.progress(

            result["new_score"]/100

        )


# COMPARISON CHART


        comparison_chart(

            result["current_prediction"],

            result["simulated_prediction"]

        )


# AI FEEDBACK


        st.markdown("## 🤖 AI Wellness Coach")

        improvement = result["improvement"]

        if improvement >= 20:

            st.success(f"""

### Excellent Choice ✅

Improving **{feature}** to **{target}**
has a strong positive effect.

Estimated improvement:

**{improvement:.1f}%**

Continue this habit consistently.

""")

        elif improvement >= 10:

            st.info(f"""

### Good Improvement 👍

Changing **{feature}**
helps reduce your predicted stress.

Estimated improvement:

**{improvement:.1f}%**

Keep maintaining this habit.

""")

        elif improvement > 0:

            st.warning(f"""

### Small Improvement

The change produces a slight improvement.

Estimated improvement:

**{improvement:.1f}%**

Try combining this with other healthy habits.

""")

        else:

            st.error("""

### No Improvement

The selected change does not reduce stress.

Consider improving another lifestyle factor.

""")


# SUMMARY


        st.markdown("---")

        st.markdown("### 📌 Simulation Summary")

        st.write(

            f"""
• Lifestyle Habit : **{feature}**

• Current Value : **{round(current,2)}**

• Target Value : **{round(target,2)}**

• Predicted Improvement : **{improvement:.1f}%**

• Wellness Score : **{result['new_score']}/100**
"""
        )