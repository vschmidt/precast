import json
import unittest
import subprocess
import os
from random import randint
from enum import Enum

class SubprocessReturnCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    SHELL_BUILTIN_ERROR = 2
    COMMAND_CANNOT_EXECUTE = 126
    COMMAND_NOT_FOUND = 127
    INVALID_ARGUMENT = 128
    SCRIPT_TERMINATED_BY_CTRL_C = 130
    EXIT_STATUS_OUT_OF_RANGE = 255

class TestPrecastCLIIntegration(unittest.TestCase):

    def setUp(self):
        """Set up the CLI script path."""
        self.cli_script = os.path.abspath("precast_core")
        self.parent_dir = os.path.abspath(os.path.join(self.cli_script, os.pardir))
        self.file_tests = os.path.join(self.parent_dir, "tmp_tests", "integration")

        self.create_directories()

    def create_directories(self):
        if not os.path.exists(self.file_tests):
            os.makedirs(self.file_tests)

    def run_cli(self, *args):
        """Helper function to run the CLI with subprocess."""
        result = subprocess.run(
            ["python", self.cli_script, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result
    
    def test_invalid_arguments(self):
        result = self.run_cli("incorrect argument")
        self.assertEqual(result.returncode, SubprocessReturnCode.SHELL_BUILTIN_ERROR.value)

    def test_help_argument(self):      
        result = self.run_cli("hello")

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertEqual(result.stdout, f"Hello\n")

    def test_init_with_success(self):
        project_name = "project_name"
        file_dir = os.path.join(self.file_tests, "precast.json")

        result = self.run_cli("init", "--out-dir", self.file_tests, "--name", project_name)

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertTrue(os.path.exists(file_dir))

        with open(file_dir) as file:
            content = json.loads(file.read())

            self.assertEqual(content["name"], project_name)
            
    def test_success_add_api(self):       
        file_dir = os.path.join(self.file_tests, "precast.json")

        result = self.run_cli("add", "api")

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertTrue(os.path.exists(file_dir))

        with open(file_dir) as file:
            content = json.loads(file.read())

            self.assertEqual(content["lenses"]["components"], {})
