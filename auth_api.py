from fastapi import APIRouter, Depends, HTTPException, status
from models import LoginRequest, User
import database_models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from datetime import timedelta
from auth_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from pythonlearn import create_user_tasks

router = APIRouter()

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(
        database_models.User.username == credentials.username,
        database_models.User.password == credentials.password,
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Call function from pythonlearn to create user tasks
    create_user_tasks(db)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_details": db_user}
    
@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    
    db_users = db.query(database_models.User).all()
    users_details = []
    for user in db_users:
        completed_count = db.query(database_models.UserBasedTaskCompleted).filter(
            database_models.UserBasedTaskCompleted.user_id == user.id,
            database_models.UserBasedTaskCompleted.task_completed.is_(True)
            ).count()
        
        user_obj = user
        user_obj.restart = True if completed_count > 0 else False
        users_details.append(user_obj)
    return users_details

@router.get("/user/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.username == username).first()
    if db_user:
        return db_user
    else:
        return "User not found"

@router.post("/user")
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        db.add(database_models.User(**user.model_dump(exclude={"id"})))
        db.commit()
        return user
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")
    
@router.put("/user")
def update_user(id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if db_user:
        try:
            db_user.fullName = user.fullName
            db_user.mobileNumber = user.mobileNumber
            db_user.username = user.username
            db_user.password = user.password
            db.commit()
            return "User details updated"
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")
    else:
        return "user not found"
    
@router.delete("/user")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if db_user:
        try:
            user_tasks = db.query(database_models.UserBasedTaskCompleted).filter(database_models.UserBasedTaskCompleted.user_id == db_user.id).all()
            for user in user_tasks:
                db.delete(user)
                
            db.delete(db_user)

            db.commit()
            return "User deleted"
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")
    else:
        return "user not found"