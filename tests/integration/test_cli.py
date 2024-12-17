import json
import shutil
import unittest
import subprocess
import os
import sys
import tempfile
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
        self.python_path = sys.executable
        self.cli_script_dir = os.path.abspath("precast_core")
        self.tests_dir = os.path.abspath("tests")
        self.root_dir = os.path.abspath(os.path.join(self.tests_dir, os.pardir))
        self.snapshots_dir = os.path.join(self.tests_dir, "snapshots")

        self.output_tests_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.output_tests_dir.cleanup()

    def run_cli(self, *args):
        """Helper function to run the CLI with subprocess."""
        result = subprocess.run(
            [self.python_path, self.cli_script_dir, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result

    def copy_file_to_temp_dir(self, file):
        template_file_dir = os.path.join(self.snapshots_dir, "components", file)
        new_file_dir = os.path.join(self.output_tests_dir.name, "precast.json")
        shutil.copyfile(template_file_dir, new_file_dir)
        return new_file_dir

    def test_invalid_arguments(self):
        result = self.run_cli("incorrect argument")
        self.assertEqual(
            result.returncode, SubprocessReturnCode.SHELL_BUILTIN_ERROR.value
        )

    def test_help_argument(self):
        result = self.run_cli("hello")

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertEqual(result.stdout, f"Hello\n")

    def test_init_with_success(self):
        project_name = "project_name"
        file_dir = os.path.join(self.output_tests_dir.name, "precast.json")

        result = self.run_cli(
            "init", "--out-dir", self.output_tests_dir.name, "--name", project_name
        )

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertTrue(os.path.exists(file_dir))

        with open(file_dir) as file:
            content = json.loads(file.read())

            self.assertEqual(content["name"], project_name)

    def test_success_single_add_api(self):
        api_name = "api_name"
        new_file_dir = self.copy_file_to_temp_dir("without_components.json")

        result = self.run_cli(
            "add", "api", "--name", api_name, "--precast-file", new_file_dir
        )

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertTrue(os.path.exists(new_file_dir))

        with open(new_file_dir) as file:
            content = json.loads(file.read())

            self.assertEqual(
                content["lenses"]["components"]["apis"],
                [{"name": api_name, "is_default": True}],
            )

    def test_success_multiple_add_api(self):
        api_names = ["api_name1", "api_name2"]
        new_file_dir = self.copy_file_to_temp_dir("without_components.json")

        for api in api_names:
            result = self.run_cli(
                "add", "api", "--name", api, "--precast-file", new_file_dir
            )
            self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)

        self.assertTrue(os.path.exists(new_file_dir))
        with open(new_file_dir) as file:
            content = json.loads(file.read())

            self.assertEqual(
                content["lenses"]["components"]["apis"],
                [
                    {"name": "api_name1", "is_default": True},
                    {"name": "api_name2", "is_default": False},
                ],
            )

    def test_apply_with_success(self):
        precast_file_dir = os.path.join(self.snapshots_dir, "fake_app", "precast.json")

        result = self.run_cli(
            "apply",
            "--precast-file",
            precast_file_dir,
            "--output-dir",
            self.output_tests_dir.name,
        )

        self.assertEqual(result.returncode, SubprocessReturnCode.SUCCESS.value)
        self.assertTrue(os.path.exists(self.output_tests_dir.name))
