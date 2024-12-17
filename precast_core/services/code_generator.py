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

        # Load configurations
        precast_configs = self._load_precast_configs(precast_file_dir)

        # Extract information
        apis = precast_configs.get("lenses", {}).get("components", {}).get("apis", [])
        endpoints_imports, routers_inject = self._process_apis(apis)

        # Generate main.py
        self._generate_main_py(output_dir, endpoints_imports, routers_inject, apis)

        # Generate router files
        self._generate_router_files(output_dir, apis)

    def _load_precast_configs(self, precast_file_dir: str) -> dict:
        """Load precast configuration file."""
        with open(precast_file_dir, "r") as precast_file:
            return json.load(precast_file)

    def _process_apis(self, apis: list) -> tuple:
        """Extract router names and inject statements from APIs."""
        routers = []
        routers_inject = []

        for api in apis:
            for router in api.get("routers", []):
                router_name = router.get("name")
                if router_name:
                    routers.append(router_name)
                    routers_inject.append(f"app.include_router({router_name})")

        endpoints_imports = f"from src.api.endpoints import {', '.join(routers)}"
        routers_inject_str = "\n    ".join(routers_inject) + "\n"

        return endpoints_imports, routers_inject_str

    def _generate_main_py(
        self, output_dir: str, imports: str, routers: str, apis: list
    ):
        """Generate the main.py file based on the template."""
        main_template_parameters = {
            "imports": imports,
            "routers": routers,
            "api_name": apis[0]["name"] if apis else "",
        }

        self._write_file_from_template(
            template_path=self.main_file_template,
            output_path=os.path.join(output_dir, "main.py"),
            parameters=main_template_parameters,
        )

    def _generate_router_files(self, output_dir: str, apis: list):
        """Generate router files based on the template."""
        api_dir = os.path.join(output_dir, "api")
        endpoints_dir = os.path.join(api_dir, "endpoints")
        os.makedirs(endpoints_dir, exist_ok=True)

        # Create __init__.py in endpoints directory
        open(os.path.join(api_dir, "__init__.py"), "a").close()
        open(os.path.join(endpoints_dir, "__init__.py"), "a").close()

        for api in apis:
            for router in api.get("routers", []):
                router_name = router.get("name")
                if router_name:
                    self._write_file_from_template(
                        template_path=self.router_file_template,
                        output_path=os.path.join(endpoints_dir, f"{router_name}.py"),
                        parameters={},
                    )

    def _write_file_from_template(
        self, template_path: str, output_path: str, parameters: dict
    ):
        """Write a file from a template with the given parameters."""
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            result = template.substitute(parameters)

        with open(output_path, "w") as output_file:
            output_file.write(result)
