from pydantic import BaseModel


class BaseComponent(BaseModel):
    name: str
    type: str


class Endpoint(BaseComponent):
    endpoint: str
    method: str


class Router(BaseComponent):
    precast_file: str


class ApiComponent(BaseComponent):
    precast_file: str
    is_default: bool = False
