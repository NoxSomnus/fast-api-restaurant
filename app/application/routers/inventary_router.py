from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from domain.schemas import InventorySchema
from infrastructure.models import Dish_Ingredient, Ingredient
from application.requests import CreateDish
from application import handlers
from application.response import Response
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/inventory', tags=['Inventario'])

user_dependency = Annotated[Session, Depends(get_current_user)]

@router.post('')
async def create_inventory(user: user_dependency, request: InventorySchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.create_inventory(request, db)
    return Response(code="200", status="success", message="Inventory created successfully", result=None).dict(exclude_none=True)

@router.get('/{id}')
async def get_inventory_by_id(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    inventory = handlers.get_inventory_by_id(id, db)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return Response(code="200", status="success", message="Sucess get data", result={"ingredient quantity",inventory.quantity}).dict(exclude_none=True)


@router.get('')
async def get_all_inventories(user: user_dependency, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    inventories = handlers.get_all_inventories(db)
    return Response(code="200", status="success", message="Sucess get data", result=inventories).dict(exclude_none=True)

@router.put('/{id}')  
async def update_inventory(user: user_dependency, id: int, request: InventorySchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_inventory(id, request, db)
    return Response(code="200", status="success", message="Inventory updated successfully", result=None).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_inventory(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.delete_inventory(id, db)
    return Response(code="200", status="success", message="Inventory deleted successfully", result=None).dict(exclude_none=True)