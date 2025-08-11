import os, datetime, jwt
from werkzeug.security import check_password_hash, generate_password_hash

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "120"))

# Hash the admin password for secure storage
ADMIN_PASS_HASH = generate_password_hash(ADMIN_PASS, method="pbkdf2:sha256", salt_length=16)

def verify_credentials(username: str, password: str) -> bool:
    return username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password)


def create_jwt(sub: str) -> str:
    now = datetime.datetime.utcnow()
    payload = {"sub": sub, "iat": now, "exp": now + datetime.timedelta(minutes=JWT_EXPIRES_MIN)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None