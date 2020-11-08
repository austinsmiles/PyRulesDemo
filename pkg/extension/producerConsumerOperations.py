from pkg.common.utils import log
import time

def process(function, componentMap, **args):
    return action_function_map[function](componentMap, **args)


def initialize(componentMap, **arg):
    log.info("Initialize something here")


def produce_employee_profile(componentMap,**arg):
    log.info("get the employee id list here")
    arr=[]
    for x in range(100, 120): #simulating a db/api fetch to get list of emp ids
        arr.append(x)
    log.info(f"Adding {str(arr)} to component map from producer")
    componentMap[arg['listComponent']] = arr


def consume_vehicle_details(componentMap,**arg):
    element=componentMap['employeePipelineElement']
    log.info(f"get the vehicle details here for the employee id {element}")
    #Do some other api fetch with element to receive additional data
    time.sleep(3)


def consume_company_details(componentMap,**arg):
    element = componentMap['employeePipelineElement']
    log.info(f"get the company details here for the employee  id {element}")
    # Do some other api fetch with element to receive additional data
    time.sleep(3)


action_function_map = {
    'produce_employee_profile': produce_employee_profile,
    'consume_vehicle_details': consume_vehicle_details,
    'consume_company_details': consume_company_details,
    'initialize': initialize
}