from dataclasses import dataclass
from typing import Generic, List, TypeVar
from pydantic import BaseModel

D = TypeVar('D')
T = TypeVar('T')

class ApiResponse(BaseModel, Generic[D]):
    code: str
    message: str
    data: D

class Content(BaseModel, Generic[T]):
    content: List[T]