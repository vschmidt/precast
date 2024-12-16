import json
import os
import tempfile
import shutil
import unittest

from precast_core.services.code_generator import CodeGeneratorService


class TestCodeGeneratorService(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.abspath("tests")
        self.root_dir = os.path.abspath(os.path.join(self.tests_dir, os.pardir))
        self.snapshots_dir = os.path.join(self.tests_dir, "snapshots")

        self.output_tests_dir = tempfile.TemporaryDirectory()

        self.code_generator_service = CodeGeneratorService()

    def tearDown(self):
        self.output_tests_dir.cleanup()

    def test_apply_file_with_api_success(self):
        main_file_dir = os.path.join(self.snapshots_dir, "fake_app", "main.py")
        expected_content = ""
        with open(main_file_dir, "r") as main_file:
            expected_content = main_file.read()

        precast_file_dir = os.path.join(self.snapshots_dir, "fake_app", "precast.json")

        result = self.code_generator_service.apply(
            precast_file_dir, self.output_tests_dir.name
        )

        # main.py
        self.assertEqual(result, None)
        self.assertTrue(os.path.exists(self.output_tests_dir.name))
        with open(
            os.path.join(self.output_tests_dir.name, "main.py"), "r"
        ) as main_file:
            self.assertEqual(expected_content, main_file.read())

        # routers
        os.path.exists(os.path.join(self.output_tests_dir.name, "endpoints", "__init__.py"))
        
        with open(precast_file_dir, "r") as precast_file:
            precast_file_content = json.loads(precast_file.read())
        
        for api in precast_file_content["lenses"]["components"]["apis"]:
            for router in api["routers"]:
                self.assertTrue(os.path.exists(os.path.join(self.output_tests_dir.name, "endpoints", f"{router['name']}.py")))

