from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError, JWTError
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
    try:
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

    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong'
        )


#-----------------------------------login part----------------------
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger sends email in `username`
    try:
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

        #deletion of previous refresh token of user
        
        db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user.id
        ).delete()

        db.commit()
        
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

        hashed_refresh_token = hash_password(refresh_token)

        db_token = models.RefreshToken(
            user_id=user.id,
            token=hashed_refresh_token,
            expires_at=refresh_expire
        )
        
        db.add(db_token)
        db.commit()

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax"
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
        
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong'
        )
    
    


# ---------------------- REFRESH ----------------------


@router.post("/refresh")
def refresh_token( request : Request, response: Response , db: Session = Depends(get_db)):
    
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user_id = payload.get("sub")

        
        db_tokens = db.query(models.RefreshToken).filter(      #list of objects (rows in DB)
            models.RefreshToken.user_id == user_id
        ).all()

        valid_token = None
        
        for t in db_tokens:
            if verify_password(token, t.token):
                valid_token = t
                break

        if not valid_token:
            raise HTTPException(status_code=401, detail="Token not found")
        
        expires_at = valid_token.expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        new_payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        
        new_access_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)
       
        return {
            "message": "Token refreshed",
            "access_token": new_access_token
        }

    except ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'TOKEN_EXPIRED'
        )        
        
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'Invalid Token'
        )  
        
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong'
        )
    
        
        
 #---------------------------LOGOUT--------------------------------
 
 
@router.post("/logout")
def logout(
    request : Request,
    response : Response,
    db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("refresh_token")

        if not token:
            raise HTTPException(status_code=401, detail="No token found")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")
        
        db_tokens = db.query(models.RefreshToken).filter(
            models.RefreshToken.user_id == user_id
        ).all()

        valid_token = None

        for t in db_tokens:
            if verify_password(token, t.token):
                valid_token = t
                break

        if not valid_token:
            raise HTTPException(status_code=401, detail="Token not found")

        
        db.delete(valid_token)
        db.commit()

        response.delete_cookie("refresh_token")
        
        return {
            "message": "Logged out successfully"
        }

    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Token has expired'
        )  
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )  
       
    except HTTPException as e:
        raise e    
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong'
        )        
    
    
#--------------------Protected------------------------------ validation of access token

# oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")

# @router.get('/protected')
# def verify_token(token : str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get('sub')
        
        if user_id is None:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'TOKEN_EXPIRED'
        )        
        
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'Invalid Token'
        )    
        
        
        