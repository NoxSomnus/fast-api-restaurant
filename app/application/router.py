from fastapi import APIRouter, HTTPException, Path, Depends
from infrastructure.config import SessionLocal
from sqlalchemy.orm import Session
from domain.aggregates import Recipe, Ingredient, RecipeIngredient
from infrastructure.schemas import RecipeSchema, RecipeIngredientSchema, IngredientSchema
import application.handlers
from application.response import Response

router = APIRouter()

handlers = application.handlers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/recipes', response_model=RecipeSchema)
async def create_recipe(request: RecipeSchema, db: Session = Depends(get_db)):
    handlers.create_recipe(request, db)
    return Response(code="200", status="success", message="Recipe created successfully", result=None).dict(exclude_none=True)

@router.post('/ingredients', response_model=IngredientSchema)
async def create_ingredient(request: IngredientSchema, db: Session = Depends(get_db)):
    handlers.create_ingredient(request, db)
    return Response(code="200", status="success", message="Ingredient created successfully", result=None).dict(exclude_none=True)

@router.get('/recipes/{id}', response_model=RecipeSchema)
async def get_recipe_by_id(id: int, db: Session = Depends(get_db)):
    recipe = handlers.get_recipe_by_id(id, db)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")#cambiar esto para que result muestre lo que se busco en db
    return Response(code="200", status="success", message="Sucess get data", result=None).dict(exclude_none=True)

@router.get('/ingredients/{id}', response_model=IngredientSchema)
async def get_ingredient_by_id(id: int, db: Session = Depends(get_db)):
    ingredient = handlers.get_ingredient_by_id(id, db)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found") #cambiar esto para que result muestre lo que se busco en db
    return Response(code="200", status="success", message="Sucess get data", result=None).dict(exclude_none=True)

