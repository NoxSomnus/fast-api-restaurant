from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field


class Config:
    orm_mode = True

class IngredientSchema(BaseModel):
    id: int
    name: str
    quantity: int
    created_at: Optional[str]
    updated_at: Optional[str]
    
    class Config:
        pass

class RecipeSchema(BaseModel):
    id: int
    name: str
    description: str
    instructions: str
    created_at: Optional[str]
    updated_at: Optional[str]
    ingredients: List[IngredientSchema]

    class Config:
        pass

class RecipeIngredientSchema(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: Optional[str]

    class Config:
        pass


