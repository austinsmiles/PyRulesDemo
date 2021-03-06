from flask import Flask
from pkg.common.utils import read_yaml
import json


app = Flask(__name__)

@app.route('/initializers')
def initializers():
    rules=read_yaml('../../rules/EmployeeCSVReader.yaml')
    return json.dumps(rules['Initializers'])

@app.route('/extensions')
def extensions():
    rules=read_yaml('../../rules/EmployeeCSVReader.yaml')
    return json.dumps(rules['EmployeeCSVReader']['extensionList'])


if __name__=='__main__':
    app.run()