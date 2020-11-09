from pkg import *
import time
from pkg.common.utils import log


def process(function, componentMap, **args):
    return action_function_map[function](componentMap, **args)


def add_to_pipeline(componentMap, **arg):
    pipeline_name = arg['pipelineName']
    pipeline_size = arg['pipelineSize']
    list_component_name = arg['listComponentName']
    list_component = componentMap[list_component_name] if list_component_name in componentMap else []
    pipeline = pkg.components.processComponentMap[pipeline_name]
    length = len(list_component)
    i = 0
    while i < length:
        if pipeline.qsize() < pipeline_size:
            pipeline.set_message(list_component[i])
            log.info(f"Added {list_component[i]} to pipeline [i={i}, size: {pipeline.qsize()}]")
            i = i+1
        else:
            log.info(f"Pipeline is full, sleeping for 1s [i={i}, size: {pipeline.qsize()}]")
            time.sleep(1)


def get_from_pipeline(componentMap, **arg):
    pipeline_name = arg['pipelineName']
    component_name = arg['componentName']
    pipeline = pkg.components.processComponentMap[pipeline_name]
    message = pipeline.get_message()
    log.info(f"Get {message} from pipeline. [size: {pipeline.qsize()}]")
    componentMap[component_name] = message


def set_event(componentMap, **arg):
    pipeline_name = arg['pipelineName']
    event_name = pipeline_name + '-event'
    event = pkg.components.processComponentMap[event_name]
    log.info(f'Setting event for {event_name}')
    event.set()


action_function_map = {
    'addToPipeline': add_to_pipeline,
    'getFromPipeline':get_from_pipeline,
    'setEvent': set_event
}