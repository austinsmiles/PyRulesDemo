from pkg.extension import *
from pkg.components import processComponentMap
from pkg.common.utils import log
import datetime
import json

def process(function, componentMap,**args):
    return action_function_map[function](componentMap,**args)


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
    processComponentName = arg["processComponentName"]
    kafkaConfig=pkg.components.config[clientName]
    kafkaServerUrl=kafkaConfig["host"]+":"+str(kafkaConfig["port"])
    pkg.components.processComponentMap[processComponentName] = KafkaProducer(bootstrap_servers=[kafkaServerUrl])


action_function_map = {
    'send': send,
    'initialize': initialize
}
