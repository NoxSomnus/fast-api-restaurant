from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field


class Config:
    orm_mode = True

class IngredientSchema(BaseModel):
    id: int
    name: str
    created_at: Optional[str]
    updated_at: Optional[str]
    
    class Config:
        pass

class DishSchema(BaseModel):
    id: int
    name: str
    description: str
    instructions: str
    created_at: Optional[str]
    updated_at: Optional[str]
    ingredients: List[int]

    class Config:
        pass

class DishIngredientSchema(BaseModel):
    dish_id: int
    ingredient_id: int

    class Config:
        pass


class MenuSchema(BaseModel):
    id: int
    name: str
    created_at: Optional[str]

    class Config:
        pass

class MenuDishSchema(BaseModel):
    menu_id: int
    dish_id: int

    class Config:
        pass

