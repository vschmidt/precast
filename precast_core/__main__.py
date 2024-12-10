
from cli import PrecastCLI
from services.file_manager import PrecastManagerService

if __name__=="__main__":
    # Services
    precast_manager_service = PrecastManagerService()

    # CLI
    cli = PrecastCLI(precast_manager_service)
    cli.run()

