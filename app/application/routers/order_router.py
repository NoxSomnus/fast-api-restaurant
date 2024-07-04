from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from domain.schemas import OrderSchema
from application import handlers
from application.response import Response
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/order', tags=['Ordenes'])

user_dependency = Annotated[Session, Depends(get_current_user)]

@router.post('')
async def create_order(user: user_dependency, request: OrderSchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.create_order(request, db)
    return Response(code="200", status="success", message="Order created successfully", result=None).dict(exclude_none=True)

@router.get('/{id}')
async def get_order_by_id(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    order = handlers.get_order_by_id(id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(code="200", status="success", message="Sucess get data", result=order).dict(exclude_none=True)

@router.get('/user/{user_id}')
async def get_orders_by_user_id(user: user_dependency, user_id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = handlers.get_orders_by_user_id(user_id, db)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return Response(code="200", status="success", message="Sucess get data", result=orders).dict(exclude_none=True)

@router.put('/{id}')  
async def update_order(user: user_dependency, id: int, status: str, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_order(id, status, db)
    return Response(code="200", status="success", message="Order updated successfully", result=None).dict(exclude_none=True)