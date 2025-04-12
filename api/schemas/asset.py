from pydantic import BaseModel


class CreateAssetRequest(BaseModel):
    code: str
    name: str
