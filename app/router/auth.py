from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import BaseModel

from app import models, schemas
from app.database import get_db
from app.utils.security import hash_password, verify_password, encrypt_password
from app.utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


router= APIRouter(prefix="/auth", tags=["Auth"])

#signup part
@router.post("/signup", response_model= schemas.UserResponse)
def signup(
    user: schemas.UserCreate,
    db: Session= Depends(get_db)
):
    existing_user= db.query(models.User).filter(
        models.User.email==user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Email already registered"
        )
    
    new_user= models.User(
        name= user.name,
        email= user.email,
        hashed_password= hash_password(user.password),
        smtp_password = encrypt_password(user.smtp_password)

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



#-----------------------------------login part----------------------
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger sends email in `username`
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "exp": expire
    }

    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    
    refresh_expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_payload = {
        "sub": str(user.id),
        "exp": refresh_expire,
        "type": "refresh"
    }

    refresh_token = jwt.encode(
        refresh_payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ---------------------- REFRESH ----------------------


class RefreshRequest(BaseModel):  # gets json token , convert into str
    refresh_token: str

@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        token = data.refresh_token

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")

       
        new_expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        new_payload = {
            "sub": user_id,
            "exp": new_expire
        }

        new_access_token = jwt.encode(
            new_payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
 