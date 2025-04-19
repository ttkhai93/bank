from typing import Any, Literal


from pydantic import BaseModel


class JSONResponseBody(BaseModel):
    status: Literal["success", "error"]
    data: dict[str, Any] = None  # Required If status = "success"
    message: str = None  # Required If status = "error"

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_unset=True)
