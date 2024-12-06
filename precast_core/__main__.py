
from cli import PrecastCLI
from services.template import TemplateService

if __name__=="__main__":
    # Services
    template_service = TemplateService()

    # CLI
    cli = PrecastCLI(template_service)
    cli.run()

