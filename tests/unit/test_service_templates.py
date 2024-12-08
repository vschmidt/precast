import json
import os
import unittest
import uuid

from precast_core.services.file_manager import FileManagerService

class TestPrecastCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.template_folder = os.path.abspath("tests")
        self.parent_dir = os.path.abspath(os.path.join(self.template_folder, os.pardir))
        self.output_folder_tests = os.path.join(self.parent_dir, "tmp_tests", "unit")       
        
        self.file_manager_service = FileManagerService()
        self.create_directories()

    def create_directories(self):
        if not os.path.exists(self.output_folder_tests):
            os.makedirs(self.output_folder_tests)

    def test_generate_init_file_string_with_success(self):
        parameters = {
            "name": "project_name"
        }
        random_out_file_name = f"{uuid.uuid4()}.json"
        precast_file_path = os.path.join(self.output_folder_tests, random_out_file_name)        

        result = self.file_manager_service.generate_init_file(precast_file_path, parameters)

        with open(precast_file_path, "r") as file:
            out_file_data = json.loads(file.read())

            self.assertEqual(out_file_data["name"], parameters["name"])
    