from sqlmodel import SQLModel, Field, create_engine
from pydantic import BaseModel, EmailStr, field_validator

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
engine = create_engine(DATABASE_URL, echo=True)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str

def create_db():
    SQLModel.metadata.create_all(engine)

class UserIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_min_length(cls, v):
        if len(v) < 5:
            raise ValueError("Şifre en az 5 karakter olmalı.")
        return v

class Token(BaseModel):
    access_token: str
    refresh_token: str   #refresh token ekledik.
    token_type: str

class UserUpdate(UserIn):
    pass

class RefreshTokenRequest(BaseModel):
    refresh_token: str