from pkg.extension import *
from pkg.components import componentMap
from pkg.common.utils import log


def process(function, **args):
    return action_function_map[function](**args)

def createSingleKey(**args):
    mKey = {}
    if args["matchType"] == 'equals':
        mKey[args["keyAttributeName"]] = str(
            componentMap[args["keyAttributeValueComponentName"]][args["keyAttributeValueComponentAttribute"]])
    elif args["matchType"] == 'startsWith':
        valDict = {}
        valDict["$regex"] = "^" + str(componentMap[args["keyAttributeValueComponentName"]][
                                          args["keyAttributeValueComponentAttribute"]])
        mKey[args["keyAttributeName"]] = valDict
    return mKey


def createKey(**args):
    mKey = {}
    for attrib in args["keyAttributeList"].values():
        mKey.update(process(function=attrib["operation"], **attrib))
    componentMap[args["keyName"]] = mKey


def read(**args):
    mKey = componentMap[args["keyName"]]
    mCol = mongoDb[args["collectionName"]]
    cur = mCol.find(mKey, {'_id': 0})
    compList=[]
    for x in cur:
        compList.append(x)
    componentMap[args["componentName"]]=compList


action_function_map = {
    'read': read,
    'createKey': createKey,
    'createSingleKey': createSingleKey
}
