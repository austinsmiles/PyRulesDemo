from pkg.components import componentMap


def process(function, **args):
    return action_function_map[function](**args)


def printArg(**arg):
    print("Src component : " + componentMap[arg["sourceComponent"]]["brand"] + "--" +
          componentMap[arg["sourceComponent"]]["model"]
          + "--" + str(componentMap[arg["sourceComponent"]]["year"]) + "--" + str(
        componentMap[arg["sourceComponent"]]["label"]))
    print("Dst component : " + componentMap[arg["destinationComponent"]]["brand"] + "--" +
          componentMap[arg["destinationComponent"]]["model"]
          + "--" + str(componentMap[arg["destinationComponent"]]["year"]) + "--" + str(
        componentMap[arg["destinationComponent"]]["label"]))


def copy(**arg):
    print("Before mapping:")
    printArg(**arg)
    componentMap[arg["destinationComponent"]][arg["destinationAttribute"]] \
        = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]]
    print("After mapping:")
    printArg(**arg)


def create(**arg):
    componentMap[arg["componentName"]] = arg["componentValue"]


def equals(**arg):
    if "destinationValue" in arg:
        print("sourceComponent attrib :  " + str(componentMap[arg["sourceComponent"]][arg["sourceAttribute"]]))
        print("dest val :" + str(arg["destinationValue"]))
        retval = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]] == arg["destinationValue"]
        print("retval : " + str(retval))
        return retval
    elif "destinationComponent" in arg and "destinationAttribute" in arg:
        print("dest comp and attrib is present")
        retval = componentMap[arg["sourceComponent"]][arg["sourceAttribute"]] == \
                 componentMap[arg["destinationComponent"]][arg["destinationAttribute"]]
        print("retval : " + str(retval))
        return retval


def validation(**arg):
    print("validation start")
    if arg["validationType"] == "ALL":
        result = True
        for condition in arg["conditionList"].values():
            result = process(function=condition["operation"], **condition)
            print("result (loop) : " + str(result))
            if result is False: break
        print("result : " + str(result))
        if result is True:
            for action in arg["actionList"].values():
                process(function=action["operation"], **action)

    if arg["validationType"] == "ANY":
        result = False
        for condition in arg["conditionList"].values():
            result = process(function=condition["operation"], **condition)
            print("result (loop) : " + str(result))
            if result is True: break
        print("result : " + str(result))
        if result is True:
            for action in arg["actionList"].values():
                process(function=action["operation"], **action)


action_function_map = {
    'copy': copy,
    'create': create,
    'equals': equals,
    'validation': validation
}
