
FEATURE_DATA = {

    "Screen Time": {
        "icon": "📱",
        "title": "Screen Time",
        "description": "Excessive screen exposure is contributing significantly to your predicted stress.",
        "action": "Reduce screen usage by 30–45 minutes today.",
        "time": "30 min",
        "difficulty": "Easy",
        "benefit": "Lower digital fatigue and improve concentration.",
        "motivation": "Small reductions in screen time can noticeably improve mental wellbeing.",
        "expected_improvement": "6–12%"
    },

    "Mobility": {
        "icon": "🚶🏃🏽",
        "title": "Mobility",
        "description": "Your physical activity is lower than recommended.",
        "action": "Walk at least 2 km today.",
        "time": "20 min",
        "difficulty": "Easy",
        "benefit": "Improves mood and lowers stress hormones.",
        "motivation": "Even light exercise has measurable mental health benefits.",
        "expected_improvement": "5–10%"
    },

    "Conversation": {
        "icon": "🗣️🫱🏼‍🫲🏼",
        "title": "Social Interaction",
        "description": "Healthy conversations help reduce emotional stress.",
        "action": "Spend 20 minutes talking with a friend or family member.",
        "time": "20 min",
        "difficulty": "Easy",
        "benefit": "Improves emotional wellbeing.",
        "motivation": "Positive conversations reduce perceived stress.",
        "expected_improvement": "4–8%"
    },

    "Dark Time": {
        "icon": "💤🌙",
        "title": "Rest Pattern",
        "description": "Your rest pattern may be affecting your stress level.",
        "action": "Maintain a consistent 7–8 hour sleep schedule.",
        "time": "Daily",
        "difficulty": "Medium",
        "benefit": "Supports mental recovery.",
        "motivation": "Good sleep improves emotional resilience.",
        "expected_improvement": "8–15%"
    },

    "App Usage": {
        "icon": "📲",
        "title": "Application Usage",
        "description": "Continuous application usage contributes to cognitive overload.",
        "action": "Take a 5-minute break every hour.",
        "time": "5 min",
        "difficulty": "Very Easy",
        "benefit": "Reduces mental fatigue.",
        "motivation": "Short breaks improve focus and productivity.",
        "expected_improvement": "3–7%"
    }

}


def get_primary_driver(shap_df):

    top = shap_df.sort_values(
        "abs",
        ascending=False
    ).iloc[0]

    feature = top["Feature"]

    info = FEATURE_DATA[feature]

    return {
        "feature": feature,
        "impact": round(float(top["Impact"]), 2),
        **info
    }


def get_action_plan(shap_df):

    shap_df = shap_df.sort_values(
        "abs",
        ascending=False
    )

    plan = []

    labels = [
        "🔥 Highest Impact",
        "⚡ Moderate Impact",
        "💡 Quick Win"
    ]

    for i in range(min(3, len(shap_df))):

        feature = shap_df.iloc[i]["Feature"]

        info = FEATURE_DATA[feature]

        plan.append({

            "priority": labels[i],

            "icon": info["icon"],

            "title": info["title"],

            "action": info["action"],

            "time": info["time"],

            "difficulty": info["difficulty"],

            "benefit": info["benefit"],

            "motivation": info["motivation"],

            "expected_improvement": info["expected_improvement"]

        })

    return plan


def calculate_wellness_score(prediction):

    score = int(max(0, min(100, (5 - prediction) * 20)))

    return score


def get_stars(score):

    if score >= 90:
        return "★★★★★"

    elif score >= 75:
        return "★★★★☆"

    elif score >= 60:
        return "★★★☆☆"

    elif score >= 40:
        return "★★☆☆☆"

    else:
        return "★☆☆☆☆"