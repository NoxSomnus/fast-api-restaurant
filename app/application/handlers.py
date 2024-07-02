from sqlalchemy.orm import Session
from domain.aggregates import *
from domain.schemas import *
from application.requests import *


def create_dish(request: CreateDish, db: Session):
    # Crear el plato
    dish = Dish(name=request.name, description=request.description, instructions=request.instructions)
    db.add(dish)
    db.flush()  # Asigna un ID al plato sin hacer commit

    # Procesar los ingredientes
    for ingredient_id, quantity in zip(request.ingredients, request.ingredients_quantities):
        registered_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if registered_ingredient:
            dish_ingredient = Dish_Ingredient(
                dish_id=dish.id,
                ingredient_id=registered_ingredient.id,
                quantity=quantity
            )
            db.add(dish_ingredient)

    # Commit y refresh
    db.commit()
    db.refresh(dish)
    return dish

def get_dish_by_id(id: int, db: Session):
    dish = db.query(Dish).filter(Dish.id == id).first()
    for i in dish.ingredients:
        print(i.name)
    return dish

def create_ingredient(request: IngredientSchema, db: Session):
    ingredient = Ingredient(id=request.id,name=request.name)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_ingredient_by_id(id: int, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    return ingredient


