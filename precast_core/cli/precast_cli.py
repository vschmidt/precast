import argparse
import os
from typing import Optional

from precast_core.patterns.factories.component import ComponentFactory
from precast_core.services.code_generator import CodeGeneratorService
from precast_core.services.file_manager import PrecastManagerService
from precast_core.validators.components import (
    ApiComponent,
    RouterComponent,
    EndpointComponent,
)


class PrecastCLI:
    def __init__(
        self,
        precast_manager_service: Optional[PrecastManagerService] = None,
        code_generator_service: Optional[CodeGeneratorService] = None,
        component_factory: Optional[ComponentFactory] = None,
    ):
        self.precast_manager_service = (
            precast_manager_service or PrecastManagerService()
        )
        self.code_generator_service = code_generator_service or CodeGeneratorService()
        self.component_factory = component_factory or ComponentFactory()
        self.parser = self._initialize_parser()

    def _initialize_parser(self) -> argparse.ArgumentParser:
        """Initialize the CLI argument parser."""
        parser = argparse.ArgumentParser(
            description="Precast CLI for managing components"
        )
        subparsers = parser.add_subparsers()

        # "hello" command
        parser_hello = subparsers.add_parser("hello", help="Say hello")
        parser_hello.set_defaults(func=self.hello)

        # "init" command
        parser_init = subparsers.add_parser("init", help="Create precast.json file")
        parser_init.add_argument(
            "--name", default=os.getcwd().split(os.sep)[-1], help="Project name"
        )
        parser_init.add_argument(
            "--out-dir", default="", help="Output directory for precast.json"
        )
        parser_init.set_defaults(func=self.init_project)

        # "add" command
        parser_add = subparsers.add_parser("add", help="Add components to the project")
        subparsers_add = parser_add.add_subparsers()

        # Generic "add" sub-command
        for component_type in ["api", "router"]:
            parser_component = subparsers_add.add_parser(
                component_type, help=f"Create {component_type.capitalize()} component"
            )
            parser_component.add_argument(
                "--name",
                required=True,
                help=f"Name of the {component_type.capitalize()}",
            )
            parser_component.add_argument(
                "--precast-file",
                default="precast.json",
                help="Path to the precast.json file",
            )
            parser_component.set_defaults(func=self.add_component, type=component_type)

        # "apply" command
        parser_apply = subparsers.add_parser(
            "apply", help="Generate code from precast file"
        )
        parser_apply.add_argument(
            "--precast-file",
            default="precast.json",
            help="Path to the precast.json file",
        )
        parser_apply.add_argument(
            "--output-dir", default="src", help="Output directory for generated code"
        )
        parser_apply.set_defaults(func=self.apply)

        return parser

    def hello(self, args):
        """Print a hello message."""
        print("Hello")

    def init_project(self, args):
        """Initialize a new precast.json file."""
        init_file_path = os.path.join(args.out_dir, "precast.json")
        parameters = {"name": args.name}
        self.precast_manager_service.generate_init_file(init_file_path, parameters)

    def add_component(self, args):
        """Add a new component to the precast.json file."""
        component = self.component_factory.build_component(args)

        self.precast_manager_service.add_component(component)

    def apply(self, args):
        """Generate code based on the precast.json file."""
        self.code_generator_service.apply(args.precast_file, args.output_dir)

    def run(self):
        """Parse arguments and execute the appropriate command."""
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            self.parser.print_help()
