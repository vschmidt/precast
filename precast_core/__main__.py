
from cli import PrecastCLI
from services.file_manager import FileManagerBase

if __name__=="__main__":
    # Services
    file_manager_service = FileManagerBase()

    # CLI
    cli = PrecastCLI(file_manager_service)
    cli.run()

