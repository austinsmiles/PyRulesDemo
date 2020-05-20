print(f'Invoking __init__.py for {__name__}')
import yaml
import pkg.components

print("importing..")


def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


pkg.components.config = load_config('../../config/config.yaml')
print("Config loaded..")
for k, v in pkg.components.config.items():
    print(k, v)
import pkg.extension.componentOperations as componentOperation
import pkg.extension.transportOperations as transportOperation

extension_map = {
    'componentOperation': componentOperation,
    'transportOperation': transportOperation
}
