from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from infrastructure import models
from domain import schemas
from infrastructure.config import SessionLocal
from application import handlers

router = APIRouter(
    prefix='/auth',
    tags=['Autenticacion JWT']
)

SECRET_KEY= 'c1e3bfdf347f294e25553b0a918fb053b2fd6c858e039865e7fbf2e3b76698b1'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username:str, password:str, db):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        print("aqui")
        return False
        
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'Email': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
user_dependency = Annotated[Session, Depends(get_current_user)]

@router.get("/Login", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db:db_dependency):
    if user is  None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return{"User":user}

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: schemas.UserSchema):
    create_user_request.password = bcrypt_context.hash(create_user_request.password)
    handlers.create_user(create_user_request, db)
    return {"message": "User created"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    return{'access_token': token, 'token_type': 'bearer'}