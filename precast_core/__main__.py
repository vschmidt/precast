
from cli import PrecastCLI
from services.file_manager import FileManagerService

if __name__=="__main__":
    # Services
    file_manager_service = FileManagerService()

    # CLI
    cli = PrecastCLI(file_manager_service)
    cli.run()

