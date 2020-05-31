print(f'Invoking __init__.py for {__name__}')
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import pkg.components
from pymongo import MongoClient

