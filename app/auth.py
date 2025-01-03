from fastapi.security import HTTPBasicCredentials

def authenticate_user(username: str, password: str) -> bool:
    # Basic authentication example
    valid_username = "admin"
    valid_password = "password123"
    return username == valid_username and password == valid_password
