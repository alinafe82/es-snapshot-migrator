from pydantic import BaseModel, Field, field_validator


class Index(BaseModel):
    name: str = Field(..., min_length=1)
    size_gb: float = Field(..., ge=0)
    created_days_ago: int = Field(..., ge=0)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("index name must not be blank")
        return normalized


class IndexExclusion(BaseModel):
    index: Index
    reasons: list[str] = Field(..., min_length=1)


class Plan(BaseModel):
    repository: str = Field(..., min_length=1)
    indices: list[Index]
    excluded_indices: list[IndexExclusion] = Field(default_factory=list)
    snapshot_name: str = Field(..., min_length=1)

    @field_validator("repository", "snapshot_name")
    @classmethod
    def normalize_identifiers(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("plan identifiers must not be blank")
        return normalized
