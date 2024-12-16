from fastapi import FastAPI




def inject_routers(app: FastAPI):
    pass

orders_api = FastAPI()
inject_routers(orders_api)