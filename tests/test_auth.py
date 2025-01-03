from app.auth import authenticate_user

def test_authenticate_user_success():
    assert authenticate_user("admin", "password123") == True

def test_authenticate_user_failure():
    assert authenticate_user("invalid", "wrongpassword") == False
