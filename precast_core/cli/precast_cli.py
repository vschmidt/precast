import argparse
import os

from precast_core.services.code_generator import CodeGeneratorService
from precast_core.services.file_manager import PrecastManagerService
from precast_core.validators.components import ApiComponent


class PrecastCLI:
    def __init__(
        self,
        precast_manager_service: PrecastManagerService | None = None,
        code_generator_service: CodeGeneratorService | None = None,
    ):
        # Services
        self.precast_manager_service = precast_manager_service
        self.code_generator_service = code_generator_service

        # Parser
        self.parser = argparse.ArgumentParser(
            description="Precast CLI for creating components"
        )
        subparsers = self.parser.add_subparsers()

        # Hello
        parser_hello = subparsers.add_parser("hello", help="Say hello")
        parser_hello.set_defaults(func=self.hello)

        # Init
        parser_init = subparsers.add_parser("init", help="Create precast.json file")
        parser_init.add_argument("--name", default=os.getcwd().split("\\")[-1])
        parser_init.add_argument("--out-dir", default="")
        parser_init.set_defaults(func=self.init_project)

        # Add
        parser_add = subparsers.add_parser("add", help="Add components to project")
        subparsers_add = parser_add.add_subparsers()

        # API creation
        parser_api = subparsers_add.add_parser("api", help="Create API")
        parser_api.add_argument("--name", default="", required=True)
        parser_api.add_argument("--precast-file", default="precast.json")
        parser_api.set_defaults(func=self.add_component)

        # Apply
        parser_apply = subparsers.add_parser("apply", help="Apply precast file")
        parser_apply.add_argument("--precast-file", default="precast.json")
        parser_apply.add_argument("--output-dir", default="src")
        parser_apply.set_defaults(func=self.apply)

    def hello(self, *args, **kargs):
        print("Hello")

    def init_project(self, *args, **kargs):
        init_file_path = os.path.join(self.args.out_dir, "precast.json")
        parameters = {"name": self.args.name}
        self.precast_manager_service.generate_init_file(init_file_path, parameters)

    def add_component(self, *args, **kargs):
        api_component = ApiComponent(**(self.args.__dict__ | {"type": "api"}))

        self.precast_manager_service.add_component(api_component)

    def apply(self, *args, **kargs):
        self.code_generator_service.apply(self.args.precast_file, self.args.output_dir)

    def run(self):
        """Parse arguments and execute the appropriate command."""
        self.args = self.parser.parse_args()

        self.args.func(self.args)
