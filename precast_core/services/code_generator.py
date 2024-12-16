import os
from string import Template

class CodeGeneratorService:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.main_file_template = os.path.join(self.template_folder, "templates", "main.py")

    def apply(self, precast_file_dir:str, output_dir:str):
        """Apply the file changes"""      
        with open(os.path.join(output_dir, "main.py"), "w") as output_file:
            parameters = {
                "imports": "",
                "routers": "pass",
                "api_name": "orders_api"
            }

            with open(self.main_file_template, "r") as template_file:
                template = Template(template_file.read())
                result = template.substitute(parameters)

            output_file.write(result)                
    