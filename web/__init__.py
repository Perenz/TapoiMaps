import flask
import os
from flask import jsonify, Flask, request, make_response
import sys
from timeit import default_timer as timer
import pandas as pd
sys.path.append('C:/Users/stefa/Desktop/U-Hopper/TapoiMaps')
import logic.Evaluator
from logic import Evaluator

app = flask.Flask(__name__)
app.config['DEBUG'] = True
evalu = Evaluator.similarityEvaluator()

#Use a class where define the simEvaluator
#There, in the init i can load the files

class errorHandler(Exception):
    status_code = 400

    def __init__(self, message, statusCode = None):
        self.message = message
        if statusCode is not None:
            self.status_code = statusCode

    def to_dict(self):
        return {'Code':self.status_code, 'Message':self.message}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return errorHandler("Wrong url path", 400)

@app.errorhandler(errorHandler)
def handleError(error):
    respose = jsonify(error.to_dict())
    respose.status_code = error.status_code
    return respose

@app.route('/err')
def getErr():
    raise errorHandler("This is an error page", statusCode=404)

@app.route('/', methods=['GET', 'POST'])
@app.route('/cosine', methods=['GET', 'POST'])
def cosine():
    start = timer()

    json = request.get_json(silent=True)
    id, simValue = evalu.computeCosineSimilarity(pd.DataFrame(json, index=['test'])) 
    
    end = timer()
    print('Time for cosine: ', round(end-start,4), ' in seconds')
    return jsonify({'id':id, 'value':round(simValue,3)})

@app.route('/euclidean', methods=['GET', 'POST'])
def euclidean():
    start = timer()
    json = request.get_json(silent=True)
    id, simValue = evalu.computeEuclideanDist(pd.DataFrame(json, index=['test'])) 

    end = timer()
    print('Time for Euclidean: ', round(end-start,4), ' in seconds')

    return jsonify({'id':id, 'value':round(simValue,3)})

@app.route('/naive', methods=['GET', 'POST'])
def naive():
    start = timer()
    json = request.get_json(silent=True)
    id, simValue = evalu.computeNaiveDist(pd.DataFrame(json, index=['test'])) 

    end = timer()
    print('Time for Naive: ', round(end-start,4), ' in seconds')

    return jsonify({'id':id, 'value':round(simValue,3)})

@app.route('/jaccard', methods=['GET', 'POST'])
def jaccard():
    start = timer()

    json = request.get_json(silent=True)
    
    id, simValue = evalu.computeJaccardDist(pd.DataFrame(json, index=['test'])) 
    end = timer()
    print('Time for jaccard: ', round(end-start,4), ' in seconds')
    return jsonify({'id':id, 'value':round(simValue,3)})

app.run()