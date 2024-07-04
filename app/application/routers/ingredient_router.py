from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from application import handlers
from application.response import Response
from domain.schemas import IngredientSchema
from infrastructure.config import SessionLocal
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/ingredients', tags=['Ingredientes'])

user_dependency = Annotated[Session, Depends(get_current_user)]

# Agregar Ingrediente
@router.post('')
async def create_ingredient(user: user_dependency, request: IngredientSchema, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.create_ingredient(request, db)
    return Response(code="200", status="success", message="Ingredient created successfully", result=None).dict(exclude_none=True)


# Obtener Ingrediente por ID
@router.get('/{id}', response_model=Response)
async def get_ingredient_by_id(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    ingredient = handlers.get_ingredient_by_id(id, db)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found") 
    return Response(code="200", status="success", message="Sucess get data", result={ingredient.id,ingredient.name}).dict(exclude_none=True)


# Obtener todos los ingredientes
@router.get('')
async def get_all_ingredients(user: user_dependency, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    ingredients = handlers.get_all_ingredients(db)
    return Response(code="200", status="success", message="Sucess get data", result=ingredients).dict(exclude_none=True)


# Actualizar Ingrediente
@router.put('/{id}')
async def update_ingredient(user: user_dependency, id: int, request: str, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_ingredient(id, request, db)
    return Response(code="200", status="success", message="Ingredient updated successfully", result=None).dict(exclude_none=True)


# Eliminar Ingrediente
@router.delete('/{id}')
async def delete_ingredient(user: user_dependency, id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.delete_ingredient(id, db)
    return Response(code="200", status="success", message="Ingredient deleted successfully", result=None).dict(exclude_none=True)