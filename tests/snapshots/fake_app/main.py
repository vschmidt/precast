from fastapi import FastAPI

from src.api.endpoints import orders_router


def inject_routers(app: FastAPI):
    app.include_router(orders_router)


orders_api = FastAPI()
inject_routers(orders_api)
