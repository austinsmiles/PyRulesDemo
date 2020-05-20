print(f'Invoking __init__.py for {__name__}')
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import pkg.components

# kafka=pkg.components.config["kafka"]
# print(f"Initializing kafka producer @ broker "+pkg.components.config["kafka"]["host"]+":"+str(pkg.components.config["kafka"]["port"]))
# kafkaServerUrl=pkg.components.config["kafka"]["host"]+":"+str(pkg.components.config["kafka"]["port"])
# kafkaProducer = KafkaProducer(bootstrap_servers=[kafkaServerUrl])