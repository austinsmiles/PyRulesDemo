from pkg.extension import *
from pkg.components import processComponentMap
from pkg.common.utils import log
from kafka import KafkaProducer
import datetime
import json

def process(function, componentMap,**args):
    return action_function_map[function](componentMap,**args)

def logStatus(processComponentName, status):
    statusDict={processComponentName:status}
    statusList=pkg.components.processComponentMap["status"]
    statusList.append(statusDict)

def send(componentMap,**arg):
    processComponentName = arg["processComponentName"]
    now = datetime.datetime.now()
    nowDict={}
    nowDict["time"] = now.strftime("%c")
    msg = json.dumps(componentMap[arg["componentName"]])
    msgtime=json.dumps(nowDict)
    log.info(f"Msg to send: {msg}")
    kafkaProducer=pkg.components.processComponentMap[processComponentName]
    future = kafkaProducer.send(arg["topicName"], msg.encode('ascii'))
    future = kafkaProducer.send(arg["topicName"], msgtime.encode('ascii'))
    kafkaProducer.flush()

def initialize(componentMap,**arg):
    clientName=arg["configName"]
    if clientName not in pkg.components.config:
        log.error(f"Config {clientName} does not exist. Please check your initialization block")
        logStatus(arg["processComponentName"], "FAILURE")
        return
    processComponentName = arg["processComponentName"]
    kafkaConfig=pkg.components.config[clientName]
    kafkaServerUrl=kafkaConfig["host"]+":"+str(kafkaConfig["port"])
    try:
        pkg.components.processComponentMap[processComponentName] = KafkaProducer(bootstrap_servers=[kafkaServerUrl])
        logStatus(arg["processComponentName"], "SUCCESS")
    except:
        log.error("Cannot connect to kafka broker.")
        logStatus(arg["processComponentName"], "FAILURE")



action_function_map = {
    'send': send,
    'initialize': initialize
}
