print(f'Invoking __init__.py for {__name__}')
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import pkg.components
from pymongo import MongoClient

if "kafka" in pkg.components.config:
    kafka=pkg.components.config["kafka"]
    kafkaServerUrl=pkg.components.config["kafka"]["host"]+":"+str(pkg.components.config["kafka"]["port"])
    kafkaProducer = KafkaProducer(bootstrap_servers=[kafkaServerUrl])

if "mongo" in pkg.components.config:
    client = MongoClient("mongodb://"+pkg.components.config["mongo"]["host"]+":"+str(pkg.components.config["mongo"]["port"]))
    mongoDb = client[pkg.components.config["mongo"]["database"]]