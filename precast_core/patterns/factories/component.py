from precast_core.validators.components import (
    ApiComponent,
    BaseComponent,
    EndpointComponent,
    RouterComponent,
)


class ComponentFactory:
    def __init__(self):
        self.component_classes = {
            "api": ApiComponent,
            "router": RouterComponent,
            "endpoint": EndpointComponent,
        }

    def build_component(self, args) -> BaseComponent:
        component_class = self.component_classes.get(args.type)
        if not component_class:
            raise ValueError(f"Unsupported component type: {args.type}")

        component_data = {
            "type": args.type,
            "name": args.name,
        }

        if args.type == "api":
            component_data["precast_file"] = args.precast_file
            component_data["is_default"] = getattr(args, "is_default", False)
            component_data["routers"] = getattr(args, "routers", [])
        elif args.type == "router":
            component_data["precast_file"] = args.precast_file
            component_data["api"] = getattr(args, "api", None)
        elif args.type == "endpoint":
            component_data["endpoint"] = args.endpoint
            component_data["method"] = args.method

        return component_class(**component_data)
