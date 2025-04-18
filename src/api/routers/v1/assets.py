from typing import Annotated

from fastapi import Query

from src.domain.services import asset_service
from src.api import StandardAPIRouter
from src.api.schemas import CommonQueryParams
from src.api.schemas.asset import CreateAssetRequest

router = StandardAPIRouter(prefix="/assets", tags=["Assets"])


@router.get("")
async def get_assets(query: Annotated[CommonQueryParams, Query()]):
    assets = await asset_service.get_assets(**query.model_dump())
    return {"assets": assets}


@router.post("")
async def create_asset(body: CreateAssetRequest):
    asset = await asset_service.create_asset(body.model_dump())
    return {"asset": asset}
