from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ComponentTypes(Enum):
    ENDPOINT = 0
    ROUTER = 1
    API = 2
    BASE = -1


class BaseComponent(BaseModel):
    name: str
    type: int = ComponentTypes.BASE

    def to_precast_fields(self):
        pass


class EndpointComponent(BaseComponent):
    endpoint: str
    method: str


class RouterComponent(BaseComponent):
    precast_file: str
    is_default: bool = False
    api: Optional[str]

    def to_precast_fields(self):
        return {"name": self.name}


class ApiComponent(BaseComponent):
    precast_file: str
    is_default: bool = False
    routers: list = []

    def to_precast_fields(self):
        return {
            "name": self.name,
            "is_default": self.is_default,
            "routers": self.routers,
        }
