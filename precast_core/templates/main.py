from fastapi import FastAPI

$imports


def inject_routers(app: FastAPI):
    $routers

$api_name = FastAPI()
inject_routers($api_name)
