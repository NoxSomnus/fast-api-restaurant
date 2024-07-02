from fastapi import APIRouter, HTTPException, Path, Depends
from infrastructure.config import SessionLocal
from sqlalchemy.orm import Session
from domain.aggregates import *
from domain.schemas import *
import application.handlers
from application.response import Response
from application.requests import *

router = APIRouter()

handlers = application.handlers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/dishes')
async def create_dish(request: CreateDish, db: Session = Depends(get_db)):
    handlers.create_dish(request, db)
    return Response(code="200", status="success", message="Dish created successfully", result=None).dict(exclude_none=True)

@router.post('/ingredients')
async def create_ingredient(request: IngredientSchema, db: Session = Depends(get_db)):
    handlers.create_ingredient(request, db)
    return Response(code="200", status="success", message="Ingredient created successfully", result=None).dict(exclude_none=True)

@router.get('/dishes/{id}', response_model=Response)
async def get_dish_by_id(id: int, db: Session = Depends(get_db)):
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
    }
    return Response(code="200", status="success", message="Sucess get data", result=result).dict(exclude_none=True)

@router.get('/ingredients/{id}', response_model=Response)
async def get_ingredient_by_id(id: int, db: Session = Depends(get_db)):
    ingredient = handlers.get_ingredient_by_id(id, db)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found") #cambiar esto para que result muestre lo que se busco en db
    return Response(code="200", status="success", message="Sucess get data", result={ingredient.id,ingredient.name}).dict(exclude_none=True)

