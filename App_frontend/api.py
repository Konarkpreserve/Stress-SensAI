import requests

BASE_URL = "http://127.0.0.1:8000"


# AUTH

def login(email: str, password: str):

    response = requests.post(

        f"{BASE_URL}/login",

        json={
            "email": email,
            "password": password
        }

    )

    return response


def register(name: str, email: str, password: str):

    response = requests.post(

        f"{BASE_URL}/register",

        json={
            "name": name,
            "email": email,
            "password": password
        }

    )

    return response



# PROFILE


def get_profile(token: str):

    response = requests.get(

        f"{BASE_URL}/profile",

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response


def update_profile(token: str, name: str):

    response = requests.put(

        f"{BASE_URL}/profile",

        json={
            "name": name
        },

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response



# PREDICTION


def predict(token: str, payload: dict):

    response = requests.post(

        f"{BASE_URL}/predict",

        json=payload,

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response



# HISTORY


def get_history(token: str):

    response = requests.get(

        f"{BASE_URL}/history",

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response



# ANALYTICS


def get_analytics(token: str):

    response = requests.get(

        f"{BASE_URL}/analytics",

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response



# WHAT-IF SIMULATOR


def simulate(token: str, payload: dict):

    response = requests.post(

        f"{BASE_URL}/simulate",

        json=payload,

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response



# TEST TOKEN


def test_token(token: str):

    response = requests.get(

        f"{BASE_URL}/test-token",

        headers={
            "Authorization": f"Bearer {token}"
        }

    )

    return response