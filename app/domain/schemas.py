from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, constr

class IngredientSchema(BaseModel):
    id: int
    name: str

class DishSchema(BaseModel):
    id: int
    name: str
    description: str
    instructions: str
    ingredients: List[int]
    menu_id: int

class DishIngredientSchema(BaseModel):
    dish_id: int
    ingredient_id: int


class MenuSchema(BaseModel):
    id: int
    name: str
    description: str

class InventorySchema(BaseModel):
    ingredient_id: int
    quantity: int


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    password: str
    role: str

class OrderSchema(BaseModel):
    id: int
    user_id: int
    dish_id: int
    quantity: int
    status: str


