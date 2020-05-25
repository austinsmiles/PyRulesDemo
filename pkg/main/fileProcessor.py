from pkg import *
from pkg.common.utils import read_yaml
from pkg.common.utils import log
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import csv
from pkg.components import componentMap

rules = read_yaml('../../rules/EmployeeCSVReader.yaml')

# send this as a cmd line arg for the process to start

processName = "EmployeeCSVReader"


def fileWatcher():
    observer = Observer()
    eventHandler = FileSystemEventHandler()
    eventHandler.on_created = fileSystemEventHandler
    observer.schedule(eventHandler, rules[processName]["directory"], recursive=True)
    observer.start()
    log.info("File watcher started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def fileSystemEventHandler(event):
    log.info(f"on_any_event called {event.src_path}")
    # if event.eventType == 'created' or event.eventType == 'modified':
    with open(event.src_path, 'r') as file:
        csvRec = csv.DictReader(file)
        for rec in csvRec:
            componentMap[rules[processName]["componentName"]] = rec
            for rule in rules[processName]["extensionList"].values():
                extension_map[rule["extension"]].process(function=rule["operation"], **rule)


fileWatcher()
