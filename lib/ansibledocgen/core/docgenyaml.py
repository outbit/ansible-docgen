import yaml


class DocGenYaml(object):
    @staticmethod
    def load(data):
        def vault_constructor(loader, node):
            # Do nothing, do not decrypt
            return "secret"
        yaml.SafeLoader.add_constructor("!vault", vault_constructor)
        return yaml.load(data, Loader=yaml.SafeLoader)
