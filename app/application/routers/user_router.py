from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from domain.schemas import UserSchema
from application import handlers
from application.response import Response
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/users', tags=['Usuarios'])

user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/{id}')
async def get_user_by_id(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = handlers.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(code="200", status="success", message="Sucess get data", result=user).dict(exclude_none=True)


@router.get('')
async def get_all_users(user: user_dependency, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    users = handlers.get_all_users(db)
    return Response(code="200", status="success", message="Sucess get data", result=users).dict(exclude_none=True)

@router.put('/{id}')  
async def update_user(user: user_dependency, id: int, request: UserSchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_user(id, request, db)
    return Response(code="200", status="success", message="User updated successfully", result=None).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_user(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.delete_user(id, db)
    return Response(code="200", status="success", message="User deleted successfully", result=None).dict(exclude_none=True)
