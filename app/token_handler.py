from itsdangerous import URLSafeTimedSerializer
from app.config import settings


SECRET_KEY = settings.secret_key
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(email):
    """Generate a time-sensitive password reset token for a given email."""
    return serializer.dumps(email, salt="password-reset-salt")

def verify_reset_token(token, expiration=3600):
    """Verify a password reset token and extract the email."""
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
        return email
    except:
        return None
