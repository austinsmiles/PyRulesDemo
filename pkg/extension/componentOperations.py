from pkg.components import componentMap
from pkg.common.utils import log


def process(function, **args):
    return action_function_map[function](**args)


def printArg(**arg):
    log.info("Src component : " + componentMap[arg["sourceComponent"]]["brand"] + "--" +
             componentMap[arg["sourceComponent"]]["model"]
             + "--" + str(componentMap[arg["sourceComponent"]]["year"]) + "--" + str(
        componentMap[arg["sourceComponent"]]["label"]))
    log.info("Dst component : " + componentMap[arg["destinationComponent"]]["brand"] + "--" +
             componentMap[arg["destinationComponent"]]["model"]
             + "--" + str(componentMap[arg["destinationComponent"]]["year"]) + "--" + str(
        componentMap[arg["destinationComponent"]]["label"]))


def copy(**arg):
    log.info("Before mapping:")
    printArg(**arg)
    componentMap[arg["destinationComponent"]][arg["destinationAttribute"]] \
        = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]]
    log.info("After mapping:")
    printArg(**arg)


def create(**arg):
    componentMap[arg["componentName"]] = arg["componentValue"]


def equals(**arg):
    if "destinationValue" in arg:
        retval = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]] == arg["destinationValue"]
        return retval
    elif "destinationComponent" in arg and "destinationAttribute" in arg:
        retval = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]] == \
                 componentMap[arg["destinationComponent"]][arg["destinationAttribute"]]
        return retval


def validation(**arg):
    if arg["validationType"] == "ALL":
        result = True
        for condition in arg["conditionList"].values():
            result = process(function=condition["operation"], **condition)
            if result is False: break
        if result is True:
            for action in arg["actionList"].values():
                process(function=action["operation"], **action)

    if arg["validationType"] == "ANY":
        result = False
        for condition in arg["conditionList"].values():
            result = process(function=condition["operation"], **condition)
            if result is True: break
        if result is True:
            for action in arg["actionList"].values():
                process(function=action["operation"], **action)


def delete(**arg):
    if "componentNameList" in arg:
        for componentName in arg["componentNameList"].split(','):
            if(componentName in componentMap):
                componentMap.pop(componentName)
            else:
                log.warning(f"Component does not exist in the componentMap. Cannot remove {componentName}")
    elif "componentName" in arg and arg["componentName"] in componentMap:
        componentMap.pop(arg["componentName"])
    else:
        log.warning(f"Component does not exist in the componentMap. Cannot remove " + arg["componentName"])


action_function_map = {
    'copy': copy,
    'create': create,
    'delete': delete,
    'equals': equals,
    'validation': validation
}
