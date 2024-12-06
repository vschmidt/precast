import os
import unittest

from precast_core.services.template import TemplateService

class TestPrecastCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.template_service = TemplateService()
        self.template_folder = os.path.abspath("tests")
        self.init_file_template = os.path.join(self.template_folder, "snapshots", "init.json")

    def test_generate_init_file_string_with_success(self):
        parameters = {
            "name": "project_name"
        }
        init_file_snapshot = ""
        with open(self.init_file_template, "r") as f:
            init_file_snapshot = f.read()


        result = self.template_service.generate_init_file(parameters)

        self.assertEqual(result, init_file_snapshot)
    