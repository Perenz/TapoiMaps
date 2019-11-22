import flask
import os
import json
from flask import jsonify, Flask, request, make_response, abort
import sys
from flask_cors import CORS
import pandas as pd
#sys.path.append(os.getcwd())
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
        '''
            Return the error messagge in a json format
        '''
        return {'Code':self.status_code, 'Message':self.message}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    raise errorHandler("Wrong url path", statusCode=400)

#Define error handler for APP with decorator
@app.errorhandler(errorHandler)
def handleError(error):
    return {'message': str(error)}, getattr(error, 'code', error.status_code)

#Example error route
@app.route('/err')
def getErr():
    raise errorHandler("This is an error page", statusCode=404)

@app.route('/similarity', methods=['GET', 'POST'])
def similarity():
    id = None
    #Get alg parameter from request url
    algorithm = request.args.get('alg', 'cosine')

    #Get profile from request body, if no json found, return error
    jsonReq = request.get_json(silent=True)
    if jsonReq is None:
        raise errorHandler("No JSON gave", statusCode=404)

    #Based on the alg parameter run a similarity evaluation algorithm
    if algorithm == '': abort(404)
    if algorithm == 'jaccard': id, simValue = evalu.computeJaccardDist(pd.DataFrame(jsonReq, index=['test'])) 
    if algorithm == 'cosine': id, simValue = evalu.computeCosineSimilarity(pd.DataFrame(jsonReq, index=['test'])) 
    if algorithm == 'euclidean': id, simValue = evalu.computeEuclideanDist(pd.DataFrame(jsonReq, index=['test'])) 
    if algorithm == 'naive': id, simValue = evalu.computeNaiveDist(pd.DataFrame(jsonReq, index=['test'])) 

    #If alg param didn't match any of the previous, return error
    if id is None:
        raise errorHandler('Invalid alg parameter', statusCode=404)

    #Else return response to the client
    return jsonify({'matches':[{'id':i} for i in id], 'metric':algorithm, 'value':round(simValue,3)})

@app.route('/profiles', methods=['DELETE'])
def deleteProfile():
    #Get request parameter representing the name/id of the loaded profile
    name = request.args.get('name', None)
    #Compose the filename + path
    filename = './computedFiles/'+name+'.json'

    if os.path.exists(filename):
        os.remove(filename)
    else:
        raise errorHandler("The specified profile does not exist", statusCode=500)

    #Apply a filter to evalu.targets to remove the deleted profile
    evalu.targets = list(filter(lambda p: p['id']!=name, evalu.targets))

    return jsonify({'message':'Profile removed correctly','id':name})


@app.route('/profiles', methods=['POST'])
def addProfile():
    #Get request body
    jsonProf = request.get_json(silent=True)
    if jsonProf is None:
        raise errorHandler("No JSON gave", statusCode=404)

    #Get request parameter representing the name/id of the loaded profile
    name = request.args.get('name', None)
    #Compose the filename + path
    filename = './computedFiles/'+name+'.json'

    #Check if filename already exists
    if(os.path.exists(filename)):
        raise errorHandler("User ID already in use, choose another one", statusCode=500)

    with open(filename, 'w') as newJson:
        json.dump(jsonProf, newJson)


    #Add the new json profile to the evaluator
    dfT = pd.DataFrame(jsonProf, index=[name])

    evalu.targets.append({'id':name, 'data':dfT})

    return jsonify({'message':'Profile added correctly','id':name})



if __name__ == '__main__':
    #Default host = 127.0.0.1
    #Default port = 5000
    app.run()