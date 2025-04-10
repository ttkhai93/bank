from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


class CommonQueryParams(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=0, le=100)
    order_by: str = None

    model_config = ConfigDict(extra="forbid")


class JSONResponseBody(BaseModel):
    status: Literal["success", "error"]
    data: dict[str, Any] = None  # Required If status = "success"
    message: str = None  # Required If status = "error"

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_unset=True)
