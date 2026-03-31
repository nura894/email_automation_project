from fastapi import Depends ,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.utils.config import  SECRET_KEY, ALGORITHM

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token: str= Depends(oauth2_scheme),
        db:Session= Depends(get_db)
):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str= payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid token"
            )
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="TOKEN_EXPIRED"
        )

    
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )    
    
    user= db.query(models.User).filter(
        models.User.id== int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            details= "User not found"
        )
    
    return user