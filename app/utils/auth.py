import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Thay bằng biến môi trường
TOKEN_EXPIRATION = 3600  # 1 giờ

def generate_token(user_id, role="user"):
    """Tạo JWT token"""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token