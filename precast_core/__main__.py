from cli import PrecastCLI
from precast_core.services.file_manager import PrecastManagerService
from precast_core.services.code_generator import CodeGeneratorService

if __name__ == "__main__":
    # Services
    precast_manager_service = PrecastManagerService()
    code_generator_service = CodeGeneratorService()

    # CLI
    cli = PrecastCLI(precast_manager_service, code_generator_service)
    cli.run()
