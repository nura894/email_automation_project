from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UpdateUserRequest
from app.utils.dependencies import get_current_user
from app.utils.security import hash_password, encrypt_password

router = APIRouter(prefix="/user", tags=["User_Update"])

from fastapi import HTTPException

def validate_and_update(field_value, field_name):
    if field_value is not None:
        value = field_value.strip()

        if value == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field_name} cannot be empty"
            )

        return value  

    return None



@router.put("/update", status_code=status.HTTP_200_OK)
def update_user(
    data: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    
    try:
        
        if not any([data.name, data.password, data.smtp_password]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided")
        
        user = db.query(User).filter(User.id == current_user.id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        name = validate_and_update(data.name, "Name")
        if name is not None:
            user.name = name
        
        password = validate_and_update(data.password, "Password")
        if password is not None:
            user.hashed_password = hash_password(password)
        
        smtp_password = validate_and_update(data.smtp_password, 'Smtp password')
        if smtp_password:
            user.smtp_password = encrypt_password(smtp_password)
            
        db.commit()
        db.refresh(user)

        return {"message": "User updated successfully"}
    
    except HTTPException as e:
        db.rollback()
        raise e
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )