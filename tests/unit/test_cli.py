from unittest import TestCase

from precast_core.cli import PrecastCLI

class TestPrecastCLI(TestCase):
    def setUp(self):
        self.precast_cli = PrecastCLI

    def test_run_without_options(self):
        pass