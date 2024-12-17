from fastapi import FastAPI

from src.api.endpoints import foo_router, bar_router


def inject_routers(app: FastAPI):
    app.include_router(foo_router)
    app.include_router(bar_router)


foo_api = FastAPI()
inject_routers(foo_api)
