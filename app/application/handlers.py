from sqlalchemy.orm import Session
from domain.aggregates import Recipe, Ingredient, RecipeIngredient
from infrastructure.schemas import RecipeSchema, RecipeIngredientSchema, IngredientSchema


def create_recipe(request: RecipeSchema, db: Session):
    recipe = Recipe(name=request.name, description=request.description, instructions=request.instructions, ingredients=request.ingredients)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_recipe_by_id(id: int, db: Session):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    return recipe

def create_ingredient(request: IngredientSchema, db: Session):
    ingredient = Ingredient(id=request.id,name=request.name, quantity=request.quantity)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_ingredient_by_id(id: int, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    return ingredient


