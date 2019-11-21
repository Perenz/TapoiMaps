import flask
import os
from flask import jsonify, Flask, request, make_response, abort
import sys
from flask_cors import CORS
from timeit import default_timer as timer
import pandas as pd
sys.path.append(os.getcwd())
import logic.Evaluator
from logic import Evaluator

app = flask.Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
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
    raise errorHandler("Wrong url path", statusCode=400)

@app.errorhandler(errorHandler)
def handleError(error):
    '''
    respose = jsonify(error.to_dict())
    respose.status_code = error.status_code
    return respose
    '''
    return {'message': str(error)}, getattr(error, 'code', 404)

@app.route('/err')
def getErr():
    raise errorHandler("This is an error page", statusCode=404)


def cosine():
    start = timer()

    json = request.get_json(silent=True)
    id, simValue = evalu.computeCosineSimilarity(pd.DataFrame(json, index=['test'])) 
    
    end = timer()
    print('Time for cosine: ', round(end-start,4), ' in seconds')
    return jsonify({'id':id, 'metric':'Cosine', 'value':round(simValue,3)})


def euclidean():
    start = timer()
    json = request.get_json(silent=True)
    id, simValue = evalu.computeEuclideanDist(pd.DataFrame(json, index=['test'])) 

    end = timer()
    print('Time for Euclidean: ', round(end-start,4), ' in seconds')

    return jsonify({'id':id,'metric':'Euclidean', 'value':round(simValue,3)})

def naive():
    start = timer()
    json = request.get_json(silent=True)
    id, simValue = evalu.computeNaiveDist(pd.DataFrame(json, index=['test'])) 

    end = timer()
    print('Time for Naive: ', round(end-start,4), ' in seconds')

    return jsonify({'id':id,'metric':'Naive', 'value':round(simValue,3), })

def jaccard():
    start = timer()

    json = request.get_json(silent=True)
    if json is None:
        raise errorHandler("No JSON gave", statusCode=404)
    
    id, simValue = evalu.computeJaccardDist(pd.DataFrame(json, index=['test'])) 
    end = timer()
    print('Time for jaccard: ', round(end-start,4), ' in seconds')
    return jsonify({'id':id, 'metric':'Jaccard', 'value':round(simValue,3)})

@app.route('/similarity', methods=['GET', 'POST'])
def similarity():
    start = timer()
    resp = None
    algorithm = request.args.get('alg', 'cosine')

    if algorithm == '': abort(404)
    if algorithm == 'jaccard': resp = jaccard()
    if algorithm == 'cosine': resp = cosine()
    if algorithm == 'euclidean': resp = euclidean()
    if algorithm == 'naive': resp = naive()

    if resp is None:
        raise errorHandler('Invalid alg parameter', statusCode=404)

    return resp

if __name__ == '__main__':
    app.run(port=5000)