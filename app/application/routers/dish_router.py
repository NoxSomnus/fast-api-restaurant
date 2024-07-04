from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth import get_current_user
from infrastructure.models import Dish_Ingredient, Ingredient
from application.requests import CreateDish
from application import handlers
from application.response import Response
from sqlalchemy.orm import Session
from infrastructure.config import get_db

router = APIRouter(prefix='/dish', tags=['Platos'])

user_dependency = Annotated[Session, Depends(get_current_user)]

@router.get('/{id}', response_model=Response)
async def get_dish_by_id(user:user_dependency,id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    dish = handlers.get_dish_by_id(id, db)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    ingredients_list = []
    dish_ingredients = db.query(Dish_Ingredient).filter(Dish_Ingredient.dish_id == dish.id).all()
    
    for dish_ingredient in dish_ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.id == dish_ingredient.ingredient_id).first()
        ingredient_data = {
            "name": ingredient.name,
            "amount": dish_ingredient.quantity
        }
        ingredients_list.append(ingredient_data)

    result = {
        "id": dish.id,
        "name": dish.name,
        "description": dish.description,
        "instructions": dish.instructions,
        "ingredients": ingredients_list,
        "menu_id": dish.menu_id
    }
    return Response(code="200", status="success", message="Sucess get data", result=result).dict(exclude_none=True)


@router.get('')
async def get_all_dishes(user:user_dependency,db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    dishes = handlers.get_all_dishes(db)
    return Response(code="200", status="success", message="Sucess get data", result=dishes).dict(exclude_none=True)

@router.post('')
async def create_dish(user:user_dependency, request: CreateDish, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.create_dish(request, db)
    return Response(code="200", status="success", message="Dish created successfully", result=None).dict(exclude_none=True)

@router.put('/{id}')
async def update_dish(user:user_dependency,id: int, request: CreateDish, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.update_dish(id, request, db)
    return Response(code="200", status="success", message="Dish updated successfully", result=None).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_dish(user:user_dependency,id: int, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    handlers.delete_dish(id, db)
    return Response(code="200", status="success", message="Dish deleted successfully", result=None).dict(exclude_none=True)
