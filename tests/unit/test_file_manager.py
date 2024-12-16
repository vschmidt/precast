import json
import os
import tempfile
import shutil
import unittest

from precast_core.services.file_manager import FileManagerBase, PrecastManagerService
from precast_core.validators.components import ApiComponent


class TestFileManagerBase(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.abspath("tests")
        self.root_dir = os.path.abspath(os.path.join(self.tests_dir, os.pardir))
        self.snapshots_dir = os.path.join(self.tests_dir, "snapshots")

        self.output_tests_dir = tempfile.TemporaryDirectory()

        self.file_manager_service = FileManagerBase()

    def tearDown(self):
        self.output_tests_dir.cleanup()

    def test_generate_init_file_with_success(self):
        parameters = {"name": "project_name"}
        precast_file_path = os.path.join(self.output_tests_dir.name, "precast.json")

        result = self.file_manager_service.generate_init_file(
            precast_file_path, parameters
        )

        self.assertIsNone(result)
        with open(precast_file_path, "r") as file:
            out_file_data = json.loads(file.read())

            self.assertEqual(out_file_data["name"], parameters["name"])

    def test_load_project_data_with_success(self):
        init_snapshot_path = os.path.join(self.snapshots_dir, "init.json")

        result = self.file_manager_service.load_project_data(init_snapshot_path)

        self.assertEqual(type(result), dict)
        self.assertEqual(result["name"], "project_name")
        self.assertEqual(type(result["lenses"]), dict)
        self.assertEqual(type(result["lenses"]["components"]), dict)
        self.assertEqual(result["lenses"]["deploy"], {})


class TestPrecastManagerService(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.abspath("tests")
        self.root_dir = os.path.abspath(os.path.join(self.tests_dir, os.pardir))
        self.snapshots_dir = os.path.join(self.tests_dir, "snapshots")

        self.output_tests_dir = tempfile.TemporaryDirectory()

        self.precast_manager_service = PrecastManagerService()

    def tearDown(self):
        self.output_tests_dir.cleanup()

    def test_add_component_with_api_success(self):
        template_file_dir = os.path.join(self.snapshots_dir, "init.json")
        new_file_dir = os.path.join(self.output_tests_dir.name, "precast.json")
        shutil.copyfile(template_file_dir, new_file_dir)
        api_component = ApiComponent(
            **{"type": "api", "precast_file": new_file_dir, "name": "api_name"}
        )

        result = self.precast_manager_service.add_component(api_component)

        self.assertEqual(result, None)

        with open(new_file_dir, "r") as file:
            content = json.loads(file.read())

            self.assertEqual(type(content), dict)
            self.assertEqual(
                content["lenses"]["components"]["apis"], [{"name": "api_name"}]
            )
