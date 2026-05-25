from pydantic import BaseModel


class Index(BaseModel):
    name: str
    size_gb: float
    created_days_ago: int


class Plan(BaseModel):
    repository: str
    indices: list[Index]
    snapshot_name: str
