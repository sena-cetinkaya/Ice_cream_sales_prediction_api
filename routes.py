from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from jose import jwt, JWTError
from models import engine, User, UserIn, UserUpdate, Token, RefreshTokenRequest
from auth import hash_password, verify_password, create_access_token, get_current_user, create_refresh_token, SECRET_KEY, ALGORITHM
import pickle

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Modeli yükle
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

@router.get("/", response_class=HTMLResponse)
def homepage(request: Request, result: float = None):
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@router.post("/estimated_profit")
def estimated_profit(temperature: int = Form(...)):
    y_pred = model.predict([[temperature]])
    result = round(y_pred.item(), 2)
    return RedirectResponse(url=f"/?result={result}", status_code=303)

@router.post("/register")
def register(user: UserIn):
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(User).where(User.email == user.email)).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")

            hashed_pwd = hash_password(user.password)
            new_user = User(email=user.email, hashed_password=hashed_pwd)
            session.add(new_user)
            session.commit()
        return {"message": "Kayıt başarılı"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Veritabanı hatası: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Beklenmeyen hata: {str(e)}")
"""def register(user: UserIn):
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == user.email)).first():
            raise HTTPException(status_code=400, detail="Email zaten kayıtlı")
        hashed_pwd = hash_password(user.password)
        session.add(User(email=user.email, hashed_password=hashed_pwd))
        session.commit()
    return {"message": "Kayıt başarılı"}"""

@router.post("/login", response_model=Token)
def login(user: UserIn):
    with Session(engine) as session:
        db_user = session.exec(select(User).where(User.email == user.email)).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Email veya şifre yanlış")
        access_token = create_access_token(data={"sub": user.email, "city": "Ankara"})
        refresh_token = create_refresh_token(data={"sub": user.email, "city": "Ankara"})  # refresh token oluşturduk
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@router.get("/secret")
def secret(current_user: User = Depends(get_current_user)):
    return {"message": f"Hoş geldin {current_user.email}, bu özel bir sayfadır!"}

@router.put("/update")
def update_user(update_data: UserUpdate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == update_data.email, User.id != current_user.id)).first():
            raise HTTPException(status_code=400, detail="Bu email başka kullanıcıda var.")
        user = session.get(User, current_user.id)
        user.email = update_data.email
        user.hashed_password = hash_password(update_data.password)
        session.add(user)
        session.commit()
    return {"message": "Bilgiler güncellendi"}

# refresh token endpoint
@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Geçersiz refresh token")

        access_token = create_access_token(data={"sub": email, "city": "Ankara"})
        new_refresh_token = create_refresh_token(data={"sub": email, "city": "Ankara"})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token doğrulanamadı")

# kişinin login olduktan sonra aldığı access token ile kendi hesabını silmesi işlemi
@router.delete("/delete")
def delete_user(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        user = session.get(User, current_user.id)
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        session.delete(user)
        session.commit()
    return {"message": "Kullanıcı başarıyla silindi"}