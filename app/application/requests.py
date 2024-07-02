from pydantic import BaseModel
from pydantic import Field
from typing import List

class CreateDish(BaseModel):
    id: int
    name: str
    description: str
    instructions: str
    ingredients: List[int]
    ingredients_quantities: List[int]
