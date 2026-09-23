from jwt import InvalidSignatureError, DecodeError
from core.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.core.database import get_db
from users.models import UserModel
from datetime import datetime,timedelta
from jose import jwt


security = HTTPBearer()

def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return None

def generate_access_token(user_id: int, expires_in: int = 3600) -> str:
    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

def get_authenticated_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) :
    token = credentials.credentials
    try :
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms = "HS256")
        user_id = decoded.get("user_id", None)
        if not user_id :
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                detail = "Authentication failed, user_id not in the payload")

        if decoded.get("type") != "access" :
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                detail = "Authentication failed, token type not valid")

        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")) :
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                detail = "Authentication failed, token expired")

        user_obj = db.query(UserModel).filter(id = user_id).one()
        return user_obj

    except InvalidSignatureError :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Authentication failed, invalid signature")
    except DecodeError :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authentication failed, decode failed")
    except Exception as e :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Authentication failed, {e}")

    return None