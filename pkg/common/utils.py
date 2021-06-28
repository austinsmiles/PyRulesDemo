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


def read_config(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def parse_fix(fix_str, fix_config, fix_map, parent='', iteration=0):
    for tag_pair in fix_str.split('|'):
        if '=' not in tag_pair:
            continue
        tag, value = int(tag_pair.split('=')[0]), tag_pair.split('=')[1]
        if tag in fix_config:
            if isinstance(fix_config[tag], str):
                if parent == '':
                    fix_map_key = fix_config[tag]
                else:
                    if int(tag) == fix_config['group_captain']:
                        iteration += 1
                    fix_map_key = parent + '.' + str(iteration) + '.' + fix_config[tag]
                fix_map[fix_map_key] = value
            elif isinstance(fix_config[tag], dict):
                if parent == '':
                    parent_key = fix_config[tag]['group_name']
                else:
                    parent_key = parent + '.' + str(iteration) + '.' + fix_config[tag]['group_name']
                group_count_key = parent_key + '.count'
                fix_map[group_count_key] = value
                for i in range(1, int(value) + 1):
                    sub_fix = fix_str.split(tag_pair)[1]
                    parse_fix(sub_fix, fix_config[tag], fix_map, parent_key)


def process_fix():
    fix_config = read_config('fix_config.yml')
    fix_str = '35=8|207=XCME|452=3|448=13432|447=12|448=2045|447=23|100=2|101=SYM|102=EXCH|101=BO|102=BBG|448=3421|447=54'
    print(f"{fix_config}")
    fix_map = {}
    parse_fix(fix_str, fix_config, fix_map)
    print(f"{fix_map}")


if __name__ == '__main__':
    process_fix()