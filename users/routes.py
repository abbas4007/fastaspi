from http.client import HTTPException
from .models import UserModel
from .schemas import UserLoginSchema, UserRegisterSchema
from core.core.database import get_db
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from auth.jwt_auth import generate_access_token

from users.schemas import UserLoginSchema
from .models import TokenModel

router = APIRouter(tags = ["users"], prefix = "/users")


def generate_token(length=32) :
    """Generate a secure random token as a string."""
    return secrets.token_hex(length)


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)) :
    user_obj = db.query(UserModel).filter_by(username = request.username.lower()).first()
    if not user_obj :
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user doesn't exists")
    if not user_obj.verify_password(request.password) :
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "password is invalid")

    # Token Based Authentication
    token_obj = TokenModel(user_id = user_obj.id, token = generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    access_token = generate_access_token(user_obj.id)

    return JSONResponse(content = {"detail" : "logged in successfully", "access_token" : access_token})


@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)) :
    if db.query(UserModel).filter_by(username = request.username).first() :
        raise HTTPException(status.HTTP_409_CONFLICT, "username already exists")
    user_obj = UserModel(username = request.username.lower(), password = request.password.lower())
    db.add(user_obj)
    db.commit()
    return JSONResponse(content = 'user register successfully')

def generate_token(length=32) :
    """Generate a secure random token as a string."""
    return secrets.token_hex(length)

# @router.post("/login")
# async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)) :
#     user_obj = db.query(UserModel).filter_by(username = request.username.lower()).first()
#     if not user_obj :
#         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user doesn't exists")
#     if not user_obj.verify_password(request.password) :
#         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "password is invalid")
#     token_obj = TokenModel(user_id = user_obj.id, token = generate_token())
#     db.add(token_obj)
#     db.commit()
#     db.refresh(token_obj)
#     return JSONResponse(content = {"detail" : "logged in successfully", "token" : token_obj.token})
#
#
# @router.post("/register")
# async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)) :
#     if db.query(UserModel).filter_by(username = request.username).first() :
#         raise HTTPException(status.HTTP_409_CONFLICT, "username already exists")
#     user_obj = UserModel(username = request.username.lower(), password = request.password.lower())
#     db.add(user_obj)
#     db.commit()
#     return JSONResponse(content = 'user register successfully')
