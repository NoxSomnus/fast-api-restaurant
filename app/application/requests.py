from domain.schemas import RecipeSchema
from pydantic import Field

class RequestRecipe:
    parameter: RecipeSchema = Field(...)