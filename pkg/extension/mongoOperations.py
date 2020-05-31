from pkg.extension import *
from pkg.components import processComponentMap
from pkg.common.utils import log


def process(function,componentMap, **arg):
    return action_function_map[function](componentMap,**arg)

def createSingleKey(componentMap,**arg):
    mKey = {}
    if arg["matchType"] == 'equals':
        mKey[arg["keyAttributeName"]] = str(
            componentMap[arg["sourceComponentName"]][arg["sourceComponentAttribute"]])
    elif arg["matchType"] == 'startsWith':
        valDict = {}
        valDict["$regex"] = "^" + str(componentMap[arg["sourceComponentName"]][
                                          arg["keyAttributeValueComponentAttribute"]])
        mKey[arg["keyAttributeName"]] = valDict
    return mKey


def createKey(componentMap,**arg):
    mKey = {}
    for attrib in arg["keyAttributeList"].values():
        mKey.update(process(function=attrib["operation"], componentMap=componentMap,**attrib))
    componentMap[arg["keyName"]] = mKey


def read(componentMap,**arg):
    mKey = componentMap[arg["keyName"]]
    processComponentName=arg["processComponentName"]
    collectionName=arg["collectionName"]
    mCol = pkg.components.processComponentMap[processComponentName][collectionName]
    cur = mCol.find(mKey, {'_id': 0})
    compList=[]
    for x in cur:
        compList.append(x)
    componentMap[arg["componentName"]]=compList

def initialize(componentMap,**arg):
    clientName=arg["configName"]
    databaseName=arg["databaseName"]
    processComponentName=arg["processComponentName"]
    client = MongoClient("mongodb://"+pkg.components.config[clientName]["host"]+":"+str(pkg.components.config[clientName]["port"]))
    pkg.components.processComponentMap[processComponentName] = client[databaseName]

action_function_map = {
    'read': read,
    'createKey': createKey,
    'createSingleKey': createSingleKey,
    'initialize':initialize
}
