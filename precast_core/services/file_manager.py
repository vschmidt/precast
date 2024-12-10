import copy
import json
import os
from string import Template

class FileManagerBase:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.init_file_template = os.path.join(self.template_folder, "templates", "init.json")

    def generate_init_file(self, precast_file_path:str, parameters:dict)->str:
        with open(precast_file_path, "w") as init_file: 
            with open(self.init_file_template, "r") as template_file:
                template = Template(template_file.read())
                result = template.substitute(parameters)

                init_file.write(result)

    def load_project_data(self, precast_file_path:str):
        with open(precast_file_path, "r") as precast_file: 
            return json.loads(precast_file.read())

class PrecastManagerService(FileManagerBase):
    def __init__(self):
        super().__init__()

    def add_component(self, parameters):
        actual_content = self.load_project_data(parameters["precast_file_path"])
        new_content = copy.deepcopy(actual_content)

        # only have API for now
        if new_content["lenses"]["components"].get("apis"):
            new_content["lenses"]["components"]["apis"].append(
                {
                    "new_api": "new_value"
                }
            )
        else:
            new_content["lenses"]["components"]["apis"] = [
               {
                   "name": parameters["name"]
               }
            ]

        with open(parameters["precast_file_path"], "w") as precast_file:
            precast_file.write(json.dumps(new_content))
