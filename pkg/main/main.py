from pkg import *
import yaml


def read_yaml(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


# rules=read_yaml('../rules/rules.yaml')
# rules=read_yaml('../../rules/validation.yaml')
rules = read_yaml('../../rules/mongoRuleSample.yaml')


for rule in rules.values():
    extension_map[rule["extension"]].process(function=rule["operation"], **rule)
