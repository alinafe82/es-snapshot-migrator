from pydantic import BaseModel, Field


class Index(BaseModel):
    name: str = Field(..., min_length=1)
    size_gb: float = Field(..., ge=0)
    created_days_ago: int = Field(..., ge=0)


class IndexExclusion(BaseModel):
    index: Index
    reasons: list[str] = Field(..., min_length=1)


class Plan(BaseModel):
    repository: str = Field(..., min_length=1)
    indices: list[Index]
    excluded_indices: list[IndexExclusion] = Field(default_factory=list)
    snapshot_name: str = Field(..., min_length=1)
