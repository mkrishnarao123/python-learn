from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import User
import database_models
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta
from auth_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 password flow sends credentials as form data: username/password.
    # In this app, username maps to user email.
    db_user = db.query(database_models.User).filter(
        database_models.User.email == form_data.username,
        database_models.User.password == form_data.password,
    ).first()
    print(db_user)
    if not db_user:
        print(db_user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires)
    print(db_user)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    
    db_users = db.query(database_models.User).all()
    return db_users

@router.get("/user/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.email == email).first()
    if db_user:
        return db_user
    else:
        return "User not found"

@router.post("/user")
def create_user(user: User, db: Session = Depends(get_db)):
    db.add(database_models.User(**user.model_dump()))
    db.commit()
    return user
    
@router.put("/user")
def update_user(id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        return "User details updated"
    else:
        return "user not found"
    
@router.delete("/user")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return "User deleted"
    else:
        return "user not found"
