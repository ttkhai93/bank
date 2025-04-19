from pydantic import BaseModel, Field, ConfigDict


class CommonQueryParams(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=0, le=100)
    order_by: str = None

    model_config = ConfigDict(extra="forbid")
