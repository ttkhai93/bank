from typing import Any
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict


class CommonQueryParams(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=0, le=100)
    order_by: str = None

    model_config = ConfigDict(extra="forbid")


class JSONResponseBodyStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"


class JSONResponseBody(BaseModel):
    status: JSONResponseBodyStatus
    data: dict[str, Any] = None  # Required If status = "success"
    message: str = None  # Required If status = "error"
