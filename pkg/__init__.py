print(f'Invoking __init__.py for {__name__}')

import pkg.components
from pkg.common.utils import read_yaml

pkg.components.config = read_yaml('config/config.yaml')

import pkg.extension.componentOperations as componentOperation
import pkg.extension.transportOperations as transportOperation
import pkg.extension.mongoOperations as mongoOperation
import pkg.extension.producerConsumerOperations as producerConsumerOperation
import pkg.extension.pipelineOperations as pipelineOperation


extension_map = {
    'componentOperation': componentOperation,
    'transportOperation': transportOperation,
    'mongoOperation': mongoOperation,
    'pipelineOperation': pipelineOperation,
    'producerConsumerOperation': producerConsumerOperation
}
