from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# from . import models, schemas
import models as models
import schemas

import cryptocode

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_user(db: Session, username, password):
    return db.query(models.User).filter((models.User.username == username) and (models.User.password == password)).first()



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def Token_Checker(token: str):
    token_decode = cryptocode.decrypt(token, "Hello")
    return token_decode


def Token_Maker(user_username, user_password):
    token = cryptocode.encrypt(f'{user_username} {user_password}', 'Hello')
    return {"access_token": token , "token_type": "bearer"}

def registration(db: Session, user_username, user_password ):
    fake_hashed_password = Token_Maker(user_username,user_password)

    db_user = models.User(username=user_username, password=user_password, token =fake_hashed_password['access_token'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # db_user = get_user_by_username(db, username= user_username)
    return db_user
    # return 'registration complete'


# def registration(db: Session, user_username, user_password):
#     # Check if user already exists
#     db_user = get_user_by_username(db, username=user_username)
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already registered")

#     fake_hashed_password = Token_Maker(user_username, user_password)
#     db_user = models.User(username=user_username, password=user_password, token=fake_hashed_password['access_token'])
    
#     try:
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#     except Exception as e:
#         db.rollback()  # Rollback the session in case of error
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#     return db_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_token = Token_Checker(token)
    if decoded_token:
        # Here you should return user information if needed
        return decoded_token  # For simplicity, return the decoded token string
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")



    # def registration(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = cryptocode.encrypt(user.password, 'mycode')
#     db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     # return db_user
#     return 'registration complete'

# def registration(db: Session, user_username, user_password ):
#     fake_hashed_password = cryptocode.encrypt(user_password, 'mycode')
#     db_user = models.User(username=user_username, token=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#     return 'registration complete'
