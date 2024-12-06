import argparse


class PrecastCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Precast CLI for creating components")

        # Hello
        self.parser.add_argument("--hello", "-hl", type=str, required=False, help="Hello")        

    def hello(self):
        print(f"Hello {self.args.hello}")

    def run(self):
        """Parse arguments and execute the appropriate command."""
        self.args = self.parser.parse_args()

        if self.args.hello:
            self.hello()

       