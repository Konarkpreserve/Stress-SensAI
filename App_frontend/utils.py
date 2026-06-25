import pandas as pd



# COLORS


def get_risk_color(risk):

    colors = {

        "Low": "#22C55E",

        "Medium": "#EAB308",

        "High": "#EF4444"

    }

    return colors.get(risk, "#6B7280")



# PREDICTION PAYLOAD


def create_prediction_payload(

    screen,
    conversation,
    mobility,
    dark,
    app_usage

):

    return {

        "screen_time_total": float(screen),

        "average_conversation_duration": float(conversation),

        "total_distance_km": float(mobility),

        "avg_dark_time": float(dark),

        "app_usage": float(app_usage)

    }



# SIMULATION PAYLOAD


def create_simulation_payload(

    feature,

    values,

    target

):

    payload = {

        "current_screen_time": values["screen"],

        "new_screen_time": values["screen"],

        "current_conversation": values["conversation"],

        "new_conversation": values["conversation"],

        "current_mobility": values["mobility"],

        "new_mobility": values["mobility"],

        "current_dark_time": values["dark"],

        "new_dark_time": values["dark"],

        "current_app_usage": values["app"],

        "new_app_usage": values["app"]

    }

    if feature == "Screen Time":

        payload["new_screen_time"] = target

    elif feature == "Conversation":

        payload["new_conversation"] = target

    elif feature == "Mobility":

        payload["new_mobility"] = target

    elif feature == "Dark Time":

        payload["new_dark_time"] = target

    elif feature == "App Usage":

        payload["new_app_usage"] = target

    return payload



# FEATURE LIST


FEATURES = [

    "Screen Time",

    "Conversation",

    "Mobility",

    "Dark Time",

    "App Usage"

]



# SLIDER LIMITS


SLIDER_LIMITS = {

    "Screen Time": (0,600),

    "Conversation": (0,300),

    "Mobility": (0,20),

    "Dark Time": (0,12),

    "App Usage": (0,600)

}



# CURRENT VALUES


def current_values(

    screen,

    conversation,

    mobility,

    dark,

    app

):

    return {

        "screen": screen,

        "conversation": conversation,

        "mobility": mobility,

        "dark": dark,

        "app": app

    }



# FEATURE VALUE


def get_feature_value(

    feature,

    values

):

    mapping = {

        "Screen Time": values["screen"],

        "Conversation": values["conversation"],

        "Mobility": values["mobility"],

        "Dark Time": values["dark"],

        "App Usage": values["app"]

    }

    return mapping[feature]



# HISTORY DATAFRAME


def history_dataframe(history):

    if len(history)==0:

        return pd.DataFrame()

    df = pd.DataFrame(history)

    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(

            df["timestamp"]

        )

    return df



# RECENT HISTORY


def recent_history(

    history,

    limit=5

):

    df = history_dataframe(history)

    if df.empty:

        return df

    return df.tail(limit)



# STAR RATING


def stars(score):

    if score>=90:

        return "★★★★★"

    elif score>=75:

        return "★★★★☆"

    elif score>=60:

        return "★★★☆☆"

    elif score>=40:

        return "★★☆☆☆"

    return "★☆☆☆☆"



# SCORE MESSAGE


def score_message(score):

    if score>=90:

        return "Outstanding Wellness"

    elif score>=80:

        return "Excellent Wellness"

    elif score>=70:

        return "Healthy Lifestyle"

    elif score>=60:

        return "Good Progress"

    elif score>=40:

        return "Needs Improvement"

    return "High Stress"



# IMPROVEMENT COLOR


def improvement_color(value):

    if value>=20:

        return "#22C55E"

    elif value>=10:

        return "#3B82F6"

    elif value>=5:

        return "#F59E0B"

    return "#EF4444"



# GREETING


def greeting(hour):

    if hour < 12:

        return "🌅 Good Morning"

    elif hour < 17:

        return "☀️ Good Afternoon"

    return "🌙 Good Evening"



# RISK EMOJI


def risk_icon(risk):

    if risk=="Low":

        return "🟢"

    elif risk=="Medium":

        return "🟡"

    return "🔴"



# RISK BADGE


def risk_badge(risk):

    return f"{risk_icon(risk)} {risk}"



# FORMAT PERCENT


def percent(value):

    return f"{value:.1f}%"