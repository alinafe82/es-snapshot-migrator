from pydantic import BaseModel
from typing import List

class Index(BaseModel):
    name: str
    size_gb: float
    created_days_ago: int

class Plan(BaseModel):
    repository: str
    indices: List[Index]
    snapshot_name: str
