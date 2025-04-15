from typing import Annotated

from fastapi import Query

from core.services import AssetService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams
from api.schemas.asset import CreateAssetRequest

router = StandardAPIRouter(prefix="/assets", tags=["Assets"])
asset_service = AssetService()


@router.get("")
async def get_assets(query: Annotated[CommonQueryParams, Query()]):
    assets = await asset_service.get_assets(**query.model_dump())
    return {"assets": assets}


@router.post("")
async def create_asset(body: CreateAssetRequest):
    asset = await asset_service.create_asset(body.model_dump())
    return {"asset": asset}
