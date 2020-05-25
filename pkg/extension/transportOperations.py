from pkg.extension import *
from pkg.components import componentMap
from pkg.common.utils import log


def process(function, **args):
    return action_function_map[function](**args)


def send(**arg):
    msg = json.dumps(componentMap[arg["componentName"]])
    # log.info(f"Msg to send: {msg}")
    future = kafkaProducer.send(arg["topicName"], msg.encode('ascii'))
    kafkaProducer.flush()


action_function_map = {
    'send': send
}
