from typing import Any
import yaml


def load_yaml(data: str) -> Any:
    def vault_constructor(loader: yaml.SafeLoader, node: yaml.Node) -> str:
        return "secret"

    yaml.SafeLoader.add_constructor("!vault", vault_constructor)
    return yaml.load(data, Loader=yaml.SafeLoader)
