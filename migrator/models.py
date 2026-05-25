from pydantic import BaseModel, Field


class Index(BaseModel):
    name: str = Field(..., min_length=1)
    size_gb: float = Field(..., ge=0)
    created_days_ago: int = Field(..., ge=0)


class Plan(BaseModel):
    repository: str = Field(..., min_length=1)
    indices: list[Index]
    snapshot_name: str = Field(..., min_length=1)
