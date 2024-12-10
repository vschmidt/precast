import json
import os
import shutil
import unittest
import uuid

from precast_core.services.file_manager import FileManagerBase, PrecastManagerService

class TestFileManagerBase(unittest.TestCase):
    def setUp(self):
        self.template_folder = os.path.abspath("tests")
        self.parent_dir = os.path.abspath(os.path.join(self.template_folder, os.pardir))
        self.output_folder_tests = os.path.join(self.parent_dir, "tmp_tests", "unit")  
        self.snapshots_folder = os.path.join(self.template_folder, "snapshots")            
        
        self.file_manager_service = FileManagerBase()
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
    
    def test_load_project_data_with_success(self):
        init_snapshot_path = os.path.join(self.snapshots_folder, "init.json")  

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
        self.output_tests_dir = os.path.join(self.root_dir, "tmp_tests", "unit")  
        self.snapshots_dir = os.path.join(self.tests_dir, "snapshots") 

        self.precast_manager_service = PrecastManagerService()

    def test_add_component_with_api_success(self):    
        template_file_dir = os.path.join(self.snapshots_dir, "init.json")  
        new_file_dir = os.path.join(self.output_tests_dir, "precast.json")          
        shutil.copyfile(template_file_dir, new_file_dir)

        result = self.precast_manager_service.add_component(new_file_dir)

        self.assertEqual(result, None)

        with open(new_file_dir, "r") as file:
            content = json.loads(file.read())

            self.assertEqual(type(content), dict)
            self.assertEqual(content["lenses"]["components"]["apis"], [])