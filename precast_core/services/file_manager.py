import copy
import json
import os
from string import Template

from precast_core.validators.components import ApiComponent


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

    def add_component(self, api_component: ApiComponent):
        actual_content = self.load_project_data(api_component.precast_file)
        new_content = copy.deepcopy(actual_content)

        # only have API for now
        if new_content["lenses"]["components"].get("apis"):
            new_content["lenses"]["components"]["apis"].append(
                {"name": api_component.name, "is_default": False}
            )
        else:
            new_content["lenses"]["components"]["apis"] = [
                {"name": api_component.name, "is_default": True}
            ]

        with open(api_component.precast_file, "w") as precast_file:
            precast_file.write(json.dumps(new_content))
