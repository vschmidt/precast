import json
import os
import tempfile
import shutil
import unittest
import ast

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

    def get_imports(self, tree):
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imports = imports + [node.name for node in node.names]

        return set(imports)

    def test_path_are_created_when_apply_file_with_all_components_success(self):
        precast_file_dir = os.path.join(self.snapshots_dir, "fake_app", "precast.json")

        self.code_generator_service.apply(precast_file_dir, self.output_tests_dir.name)

        # main.py
        self.assertTrue(
            os.path.exists(os.path.join(self.output_tests_dir.name, "main.py"))
        )

        # apis
        self.assertTrue(
            os.path.exists(
                os.path.join(self.output_tests_dir.name, "api", "__init__.py")
            )
        )

        # routers
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.output_tests_dir.name, "api", "endpoints", "__init__.py"
                )
            )
        )

        with open(precast_file_dir, "r") as precast_file:
            precast_file_content = json.loads(precast_file.read())

        for api in precast_file_content["lenses"]["components"]["apis"]:
            for router in api["routers"]:
                self.assertTrue(
                    os.path.exists(
                        os.path.join(
                            self.output_tests_dir.name,
                            "api",
                            "endpoints",
                            f"{router['name']}.py",
                        )
                    )
                )

    def test_main_content_is_correct_when_apply_file_with_all_components_success(self):
        precast_file_dir = os.path.join(self.snapshots_dir, "fake_app", "precast.json")

        self.code_generator_service.apply(precast_file_dir, self.output_tests_dir.name)

        main_dir = os.path.join(self.output_tests_dir.name, "main.py")
        self.assertTrue(os.path.exists(main_dir))
        with open(main_dir, "r") as main_file:
            main_content = main_file.read()

        try:
            compile(main_content, "<string>", "exec")
        except SyntaxError as e:
            self.fail(f"Generated code is not valid Python: {e}")

        # have correct imports?
        expected_imports = {"FastAPI", "foo_router", "bar_router"}
        tree = ast.parse(main_content)
        imports = self.get_imports(tree)
        missing_imports = expected_imports - imports

        self.assertFalse(
            missing_imports, f"Missing imports {', '.join(missing_imports)}"
        )

    def test_router_content_is_correct_when_apply_file_with_all_components_success(
        self,
    ):
        precast_file_dir = os.path.join(self.snapshots_dir, "fake_app", "precast.json")

        self.code_generator_service.apply(precast_file_dir, self.output_tests_dir.name)

        with open(precast_file_dir, "r") as precast_file:
            precast_content = json.loads(precast_file.read())

        apis = precast_content["lenses"]["components"]["apis"]

        for api in apis:
            for router in api["routers"]:
                router_path = os.path.join(
                    self.output_tests_dir.name,
                    "api",
                    "endpoints",
                    f"{router['name']}.py",
                )
                self.assertTrue(os.path.exists(router_path))

                with open(router_path, "r") as router_file:
                    router_content = router_file.read()

                try:
                    compile(router_content, "<string>", "exec")
                except SyntaxError as e:
                    self.fail(f"Generated code is not valid Python: {e}")

                # have correct imports?
                expected_imports = {"APIRouter", "Depends", "status", "JSONResponse"}
                tree = ast.parse(router_content)
                imports = self.get_imports(tree)
                missing_imports = expected_imports - imports

                self.assertFalse(
                    missing_imports, f"Missing imports {', '.join(missing_imports)}"
                )
