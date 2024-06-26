from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class Response (GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    #result: Optional[T]