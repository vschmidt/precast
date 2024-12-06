import os
from string import Template

class TemplateService:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.init_file_template = os.path.join(self.template_folder, "templates", "init.json")

    def generate_init_file(self, parameters:dict)->str:
        result = None
        with open(self.init_file_template, "r") as f:
            template = Template(f.read())
            result = template.substitute(parameters)
        
        return result