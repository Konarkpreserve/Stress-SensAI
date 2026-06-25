import requests

login = requests.post(
    "http://127.0.0.1:8000/login",
    json={
        "email": "komal@example.com",
        "password": "123456"
    }
)

print("LOGIN RESPONSE:")
print(login.json())

token = login.json()["access_token"]

response = requests.get(
    "http://127.0.0.1:8000/test-token",
    headers={
        "Authorization": f"Bearer {token}"
    }
)

print("\nTEST TOKEN RESPONSE:")
print(response.status_code)
print(response.json())