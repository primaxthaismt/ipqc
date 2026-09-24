import sys
from fastapi.testclient import TestClient

# Add current directory to path
sys.path.insert(0, ".")

from api.index import app

client = TestClient(app)
response = client.get("/api/stations?date=2026-08-20&time_block=08:00%20-%2010:00")
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

response = client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
print(f"Login Status: {response.status_code}")
print(f"Login Response: {response.text}")
