from pkg.extension import *
from pkg.components import processComponentMap
from pkg.common.utils import log


def process(function, componentMap, **arg):
    return action_function_map[function](componentMap, **arg)


def logStatus(processComponentName, status):
    statusDict={processComponentName:status}
    statusList=pkg.components.processComponentMap["status"]
    statusList.append(statusDict)


def createSingleKey(componentMap, **arg):
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


def createKey(componentMap, **arg):
    mKey = {}
    for attrib in arg["keyAttributeList"].values():
        mKey.update(process(function=attrib["operation"], componentMap=componentMap, **attrib))
    componentMap[arg["keyName"]] = mKey

def create(componentMap, **arg):
    processComponentName = arg["processComponentName"]
    collectionName = arg["collectionName"]
    mCol = pkg.components.processComponentMap[processComponentName][collectionName]
    if type(componentMap[arg["componentName"]]) is dict:
        mCol.insert_one(componentMap[arg["componentName"]])
    elif type(componentMap[arg["componentName"]]) is list:
        mCol.insert_many(componentMap[arg["componentName"]])

def readOne(componentMap, **arg):
    mKey = componentMap[arg["keyName"]]
    processComponentName = arg["processComponentName"]
    collectionName = arg["collectionName"]
    mCol = pkg.components.processComponentMap[processComponentName][collectionName]
    elem = mCol.find_one(mKey, {'_id': 0})
    componentMap[arg["componentName"]] = elem

def read(componentMap, **arg):
    mKey = componentMap[arg["keyName"]]
    processComponentName = arg["processComponentName"]
    collectionName = arg["collectionName"]
    mCol = pkg.components.processComponentMap[processComponentName][collectionName]
    cur = mCol.find(mKey, {'_id': 0})
    compList = []
    for x in cur:
        compList.append(x)
    componentMap[arg["componentName"]] = compList


def initialize(componentMap, **arg):
    configName=arg["configName"]
    if configName not in pkg.components.config:
        log.error(f"Config {configName} does not exist. Please check your initialization block")
        logStatus(arg["processComponentName"],"FAILURE")
        return
    clientName = arg["configName"]
    databaseName = arg["databaseName"]
    processComponentName = arg["processComponentName"]
    client = MongoClient(
        "mongodb://" + pkg.components.config[clientName]["host"] + ":" + str(pkg.components.config[clientName]["port"]))
    dbnames = client.list_database_names()
    if databaseName not in dbnames:
        log.error(f"Database {databaseName} does not exist. Please check your initialization block")
        logStatus(arg["processComponentName"], "FAILURE")
        return
    pkg.components.processComponentMap[processComponentName] = client[databaseName]
    logStatus(arg["processComponentName"], "SUCCESS")


action_function_map = {
    'read': read,
    'readOne': readOne,
    'create':create,
    'createKey': createKey,
    'createSingleKey': createSingleKey,
    'initialize': initialize
}
