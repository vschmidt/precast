import json
import os
from string import Template


class CodeGeneratorService:
    def __init__(self):
        self.template_folder = os.path.abspath("precast_core")
        self.main_file_template = os.path.join(
            self.template_folder, "templates", "main.py"
        )
        self.router_file_template = os.path.join(
            self.template_folder, "templates", "router.py"
        )

    def apply(self, precast_file_dir: str, output_dir: str):
        """Apply the file changes"""
        os.makedirs(output_dir, exist_ok=True)
        # Load configs
        precast_configs = {}
        with open(precast_file_dir, "r") as precast_file:
            precast_configs = json.loads(precast_file.read())

        # extract infos
        apis = precast_configs["lenses"]["components"]["apis"]
        routers = []
        routers_inject = []
        for api in apis:
            for router in api["routers"]:
                routers.append(router["name"])
                routers_inject.append(f"app.include_router({router['name']})")

        endpoints_imports = "from src.api.endpoints import "
        endpoints_imports += ", ".join(routers)
        routers_inject = "\n    ".join(routers_inject) + "\n"

        # Main.py
        main_template_parameters = {
            "imports": endpoints_imports,
            "routers": routers_inject,
            "api_name": api["name"],
        }
        with open(os.path.join(output_dir, "main.py"), "w") as output_file:
            with open(self.main_file_template, "r") as template_file:
                template = Template(template_file.read())
                result = template.substitute(main_template_parameters)

            output_file.write(result)

        # Routers
        endpoints_file_dir = os.path.join(output_dir, "endpoints")
        os.makedirs(endpoints_file_dir)
        open(os.path.join(endpoints_file_dir, "__init__.py"), "a").close()

        for api in apis:
            for router in api["routers"]:
                endpoints_file_dir = os.path.join(output_dir, "endpoints")
                os.makedirs(endpoints_file_dir, exist_ok=True)
                with open(
                    os.path.join(endpoints_file_dir, f"{router['name']}.py"), "w"
                ) as output_file:
                    with open(self.router_file_template, "r") as template_file:
                        template = Template(template_file.read())
                        result = template.substitute(main_template_parameters)
