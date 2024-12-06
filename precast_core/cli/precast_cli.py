import argparse
import os

from services.template import TemplateService


class PrecastCLI:
    def __init__(self, template_service:TemplateService|None=None):
        # Services
        self.template_service = template_service

        # Parser
        self.parser = argparse.ArgumentParser(description="Precast CLI for creating components")
        subparsers = self.parser.add_subparsers()

        # Hello
        parser_hello = subparsers.add_parser('hello', help='Say hello')
        parser_hello.set_defaults(func=self.hello)      

        # Init
        parser_init = subparsers.add_parser('init', help='Create precast.json file')
        parser_init.add_argument("--name", default=os.getcwd().split("\\")[-1])
        parser_init.add_argument("--out-dir", default="")
        parser_init.set_defaults(func=self.init_project)

        # Create
        parser_create = subparsers.add_parser('create', help='Add components to project')
        subparsers_create = parser_create.add_subparsers()

        # API creation
        parser_api = subparsers_create.add_parser('api', help='Create API')
        parser_api.set_defaults(func=self.create_component)


    def hello(self, *args, **kargs):
        print("Hello")

    def init_project(self, *args, **kargs):
        with open(os.path.join(self.args.out_dir, "precast.json"), "w") as file:
            parameters = {
                "name": self.args.name
            }
            init_file_content = self.template_service.generate_init_file(parameters)
            file.write(init_file_content)

    def create_component(self, *args, **kargs):
        pass

    def run(self):
        """Parse arguments and execute the appropriate command."""
        self.args = self.parser.parse_args()
       
        self.args.func(self.args)
