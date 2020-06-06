from pkg import *
from pkg.components import processComponentMap
from pkg.common.utils import read_yaml
from pkg.common.utils import log
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import csv
import os
import sys
from pkg.components import processComponentMap
# send this as a cmd line arg for the process to start

def initialize():
    pkg.components.processComponentMap["rules"] = read_yaml('../../rules/' + pkg.components.processComponentMap["processName"] + '.yaml')
    initializers=pkg.components.processComponentMap["rules"]["Initializers"]
    for initializer in initializers.values():
        extension_map[initializer["extension"]].process(function=initializer["operation"], componentMap=pkg.components.processComponentMap,**initializer)
    status=pkg.components.processComponentMap["status"]
    log.info(status)
    # for rec in status:
    #     log.info(rec)

def fileWatcher():
    observer = Observer()
    eventHandler = FileSystemEventHandler()
    eventHandler.on_created = fileSystemEventHandler
    #eventHandler.on_modified = fileSystemEventHandler
    pName=pkg.components.processComponentMap["processName"]
    observer.schedule(eventHandler, pkg.components.processComponentMap["rules"][pName]["directory"], recursive=True)
    observer.start()
    log.info("File watcher started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def fileSystemEventHandler(event):
    log.info(f"Processing file {event.src_path}")
    # if event.eventType == 'created' or event.eventType == 'modified':
    pName = pkg.components.processComponentMap["processName"]
    processRules=pkg.components.processComponentMap["rules"][pName]
    time.sleep(2)
    with open(event.src_path, 'r') as file:
        csvRec = csv.DictReader(file)
        for rec in csvRec:
            componentMap={}
            componentMap[processRules["componentName"]] = rec
            for rule in processRules["extensionList"].values():
                extname = rule["extension"]
                extension_map[rule["extension"]].process(function=rule["operation"],componentMap=componentMap, **rule)
    os.remove(event.src_path)


if __name__ == '__main__':
    pkg.components.processComponentMap["processName"] = sys.argv[1]
    initialize()
    fileWatcher()
