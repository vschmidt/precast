import argparse


class PrecastCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Precast CLI for creating components")
        subparsers = self.parser.add_subparsers()

        # Hello
        parser_hello = subparsers.add_parser('hello', help='Say hello')
        parser_hello.set_defaults(func=self.hello)      

        # Init
        parser_init = subparsers.add_parser('init', help='Create precast.json file')
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
        pass

    def create_component(self, *args, **kargs):
        pass

    def run(self):
        """Parse arguments and execute the appropriate command."""
        self.args = self.parser.parse_args()
       
        self.args.func(self.args)
