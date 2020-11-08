from pkg import *
import queue
import threading
import concurrent.futures
import time
from pkg.common.utils import log

some_global_variable="some_global_value"


def initialize():
    pkg.components.processComponentMap["rules"] = read_yaml('rules/' + 'ProducerConsumer' + '.yaml')
    if "Initializers" in pkg.components.processComponentMap["rules"]:
        initializers=pkg.components.processComponentMap["rules"]["Initializers"]
        for initializer in initializers.values():
            extension_map[initializer["extension"]].process(function=initializer["operation"], componentMap=pkg.components.processComponentMap,**initializer)
        #status = pkg.components.processComponentMap["status"]
    #log.info(status)


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__()

    def get_message(self):
        value = self.get()
        return value

    def set_message(self, value):
        self.put(value)


def producer(pipeline_name, producer_name, event_name, id):
    """Pretend we're getting a number from the network."""
    processRules = pkg.components.processComponentMap["rules"][producer_name]
    event = pkg.components.processComponentMap[event_name]
    componentMap = {}
    while not event.is_set():
        for rule in processRules["extensionList"].values():
            extension_map[rule["extension"]].process(function=rule["operation"], componentMap=componentMap, **rule)



def consumer(pipeline_name, consumer_name, event_name, worker_id):
    """Pretend we're saving a number in the database."""
    processRules = pkg.components.processComponentMap["rules"][consumer_name]
    pipeline = pkg.components.processComponentMap[pipeline_name]
    event = pkg.components.processComponentMap[event_name]
    componentMap = {}
    while not event.is_set() or not pipeline.empty():
        log.info(f"Starting consumer {consumer_name}-{worker_id}")
        for rule in processRules["extensionList"].values():
            extension_map[rule["extension"]].process(function=rule["operation"], componentMap=componentMap, **rule)
    log.info(f"{consumer_name}-{worker_id} received EXIT event. Exiting")


if __name__ == "__main__":
    initialize()
    processRules = pkg.components.processComponentMap["rules"]['ProducerConsumer']
    componentMap = {}
    pipeline_name = processRules['pipelineName']
    producers = processRules['producers']
    consumers = processRules['consumers']
    event_name = pipeline_name + '-event'
    pkg.components.processComponentMap['employee-pipeline'] = Pipeline()
    pkg.components.processComponentMap['employee-pipeline-event']=threading.Event()
    max_worker_count = 0
    for k, v in producers.items():
        max_worker_count = max_worker_count + v
    for k, v in consumers.items():
        max_worker_count = max_worker_count + v
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker_count) as executor:
        for k, v in producers.items():
            for id in range(0, v):
                log.info(f"submitting producer {k}-{id + 1}")
                executor.submit(producer, pipeline_name, k, event_name, id + 1)

        for k, v in consumers.items():
            for id in range(0, v):
                log.info(f"submitting consumer {k}-{id + 1}")
                executor.submit(consumer, pipeline_name, k, event_name, id + 1)
        #time.sleep(0.1)
        pkg.components.processComponentMap[event_name].set()
    log.info(f"Max worker count is {max_worker_count}")