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
    for x in list_component:
        if pipeline.qsize() < pipeline_size-1:
            log.info(f"Adding {x} to pipeline")
            pipeline.set_message(x)
        else:
            log.info(f"Adding {x} to pipeline")
            pipeline.set_message(x)
            log.info("Pipeline is full, sleeping for 1s")
            time.sleep(1)


def get_from_pipeline(componentMap, **arg):
    pipeline_name = arg['pipelineName']
    component_name = arg['componentName']
    pipeline = pkg.components.processComponentMap[pipeline_name]
    message = pipeline.get_message()
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