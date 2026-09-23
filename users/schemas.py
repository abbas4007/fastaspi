from pydantic import BaseModel, field_validator, Field, ValidationError
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel) :
    username: str = Field(..., max_length = 250, description = "Username")
    password: str = Field(..., max_length = 250, description = "Password")


class UserRegisterSchema(BaseModel) :
    username: str = Field(..., max_length = 250, description = "Username")
    password: str = Field(..., max_length = 250, description = "Password")
    confirm_password: str = Field(..., max_length = 250, description = "Confirm Password")

    @field_validator('confirm_password')
    def check_password_match(cls, confirm_password, validation) :
        if not confirm_password == validation.data.get('password') :
            raise ValidationError('Password does not match')
        return confirm_password
