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

    def test_add_component_with_api_success(self):        
        main_file_dir = os.path.join(self.snapshots_dir, "components", "main.py")  
        expected_content = ""
        with open(main_file_dir, "r") as main_file:
            expected_content = main_file.read()
        
        all_components_file_dir = os.path.join(self.snapshots_dir, "all_components.json")       

        result = self.code_generator_service.apply(all_components_file_dir, self.output_tests_dir.name)

        self.assertEqual(result, None)
        self.assertTrue(os.path.exists(self.output_tests_dir.name))

        with open(os.path.join(self.output_tests_dir.name, "main.py"), "r") as main_file:
            self.assertEqual(expected_content, main_file.read())
        