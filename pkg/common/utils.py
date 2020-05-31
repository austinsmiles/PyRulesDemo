import logging
import inspect
import yaml

log = logging

log.basicConfig(level=log.INFO, format='%(asctime)s:%(filename)s:%(funcName)s'
                                       ':%(levelname)s :%(message)s')


def read_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
