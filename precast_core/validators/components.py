from pydantic import BaseModel


class BaseComponent(BaseModel):
    name: str
    type: str


class ApiComponent(BaseComponent):
    precast_file: str
