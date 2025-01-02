from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Mock user database
users = {"admin": "password123"}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in users or not secrets.compare_digest(users[username], password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return username
