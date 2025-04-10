from fastapi import FastAPI

from api.routers import routers


def create_app() -> FastAPI:
    new_app = FastAPI()

    for router in routers:
        new_app.include_router(router)

    return new_app


app = create_app()
