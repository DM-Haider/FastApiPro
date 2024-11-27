from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas
import crud
from engine import get_db, engine
import models

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



@router.post("/register")
def register(r_username:str, r_password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=r_username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username already registered")
    return crud.registration(db=db, user_username=r_username, user_password= r_password)



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, username=form_data.username, password=form_data.password)
    if db_user:
        return crud.Token_Maker(form_data.username, form_data.password)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
# @router.post("/login")
# def login(r_username:str, r_password: str, db: Session = Depends(get_db)):
#     db_password = crud.verify_user(db, username=r_username, password =r_password)

#     if db_password:
#         return f'token: {crud.Token_Maker(r_username,r_password)}'
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not exist")


@router.get("/")
def get_user_perm(current_user: str = Depends(crud.get_current_user)):
    return {"message": "You have permission", "user": current_user}




# @router.get("/")
# def get_user_perm():
#     ...
#     crud.Token_Checker()



# @router.post("/register")
# def register():
#     pass


# @router.post("/login")
# def login():
#     pass


# @router.get("/")
# def get_user_perm():
#     pass


# @router.post("/users/", response_model=schemas.User)
# def regestration(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="username already registered")
    # return crud.regestration(db=db, user=user)