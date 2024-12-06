import os
from string import Template

class FileManagerService:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.init_file_template = os.path.join(self.template_folder, "templates", "init.json")

    def generate_init_file(self, precast_file_path:str, parameters:dict)->str:
        with open(precast_file_path, "w") as init_file: 
            with open(self.init_file_template, "r") as template_file:
                template = Template(template_file.read())
                result = template.substitute(parameters)

                init_file.write(result)
        