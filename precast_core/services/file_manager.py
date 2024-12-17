import copy
import json
import os
from string import Template

from precast_core.validators.components import ApiComponent, BaseComponent


class FileManagerBase:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.init_file_template = os.path.join(
            self.template_folder, "templates", "init.json"
        )

    def generate_init_file(self, precast_file_path: str, parameters: dict) -> str:
        with open(precast_file_path, "w") as init_file:
            with open(self.init_file_template, "r") as template_file:
                template = Template(template_file.read())
                result = template.substitute(parameters)

                init_file.write(result)

    def load_project_data(self, precast_file_path: str):
        with open(precast_file_path, "r") as precast_file:
            return json.loads(precast_file.read())


class PrecastManagerService(FileManagerBase):
    def __init__(self):
        super().__init__()

    def add_component(self, component: BaseComponent):
        precast_content = self.load_project_data(component.precast_file)

        if component.type == "api":
            if precast_content["lenses"]["components"].get("apis"):
                precast_content["lenses"]["components"]["apis"].append(
                    component.to_precast_fields()
                )
            else:
                component.is_default = True
                precast_content["lenses"]["components"]["apis"] = [
                    component.to_precast_fields()
                ]
        elif component.type == "router":
            apis = precast_content["lenses"]["components"]["apis"]
            default_api = list(filter(lambda x: x["is_default"], apis))[0]

            if default_api.get("routers"):
                precast_content["lenses"]["components"]["apis"].append(
                    component.to_precast_fields()
                )
            else:
                component.is_default = True
                default_api["routers"] = [component.to_precast_fields()]

        with open(component.precast_file, "w") as precast_file:
            precast_file.write(json.dumps(precast_content))
