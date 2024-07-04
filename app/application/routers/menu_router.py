from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from domain.schemas import MenuSchema
from application import handlers
from application.response import Response
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/menu', tags=['Menus'])

user_dependency = Annotated[Session, Depends(get_current_user)]


@router.post('')
async def create_menu(user: user_dependency, request: MenuSchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.create_menu(request, db)
    return Response(code="200", status="success", message="Menu created successfully", result=None).dict(exclude_none=True)

@router.get('/{id}')
async def get_menu_by_id(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    menu = handlers.get_menu_by_id(id, db)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return Response(code="200", status="success", message="Sucess get data", result={menu.id,menu.name}).dict(exclude_none=True)


@router.get('')
async def get_all_menus(user: user_dependency, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    menus = handlers.get_all_menus(db)
    return Response(code="200", status="success", message="Sucess get data", result=menus).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_menu(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.delete_menu(id, db)
    return Response(code="200", status="success", message="Menu deleted successfully", result=None).dict(exclude_none=True)

@router.put('/{id}')  
async def update_menu(user: user_dependency, id: int, request: MenuSchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_menu(id, request, db)
    return Response(code="200", status="success", message="Menu updated successfully", result=None).dict(exclude_none=True)