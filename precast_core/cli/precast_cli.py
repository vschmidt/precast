import argparse


class PrecastCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Precast CLI for creating components")
        self.subparsers = self.parser.add_subparsers(help='Create component')

        # Hello
        self.parser.add_argument("--hello", "-hl", type=str, help="Hello")        

        # Init
        self.init_parser = self.subparsers.add_parser('init', help='Create precast.json file')      
        self.init_parser.add_argument(
            '--name', '-n',
            type=str,
            help='Name of project'
        )

        # Create
        self.create_parser = self.subparsers.add_parser('create', help='[API]')
        self.create_parser.add_argument(
            'type',
            type=str,
            choices=['api', 'connector', 'service', 'repository'],  # List of valid values
            help='Type of component (choices: api, connector, service, repository)'
        )


    def hello(self):
        print(f"Hello {self.args.hello}")

    def init_project(self):
        pass

    def run(self):
        """Parse arguments and execute the appropriate command."""
        self.args = self.parser.parse_args()

        if self.args.hello:
            self.hello()

       