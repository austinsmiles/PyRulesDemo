import redis
from pkg.extension import *
from pkg.components import processComponentMap
from pkg.common.utils import log


def process(function, componentMap, **arg):
    return action_function_map[function](componentMap, **arg)


def initialize(componentMap, **arg):
    processComponentName = arg["processComponentName"]
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    pkg.components.processComponentMap[processComponentName] = r


action_function_map={
    'initialize': initialize
}