import flask
import os
import json
from flask import jsonify, Flask, request
import time
from flask_cors import CORS
from logic import Evaluator

app = flask.Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
evalu = Evaluator.similarityEvaluator()

#Use a class where define the simEvaluator
#There, in the init i can load the files

class errorHandler(Exception):
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

@app.route('/similarity', methods=['GET'])
def similarity():
    start = time.time()
    id = None
    #Get alg parameter from request url
    algorithm = request.args.get('alg', 'cosine')

    #Get profile from request body, if no json found, return error
    jsonReq = request.get_json(silent=True)
    if jsonReq is None:
        raise errorHandler("No JSON gave", statusCode=400)

    #Based on the alg parameter run a similarity evaluation algorithm
    if algorithm == '': id, simValue = evalu.computeCosineSimilarity(jsonReq) 
    if algorithm == 'jaccard': id, simValue = evalu.computeJaccardDist(jsonReq) 
    if algorithm == 'cosine': id, simValue = evalu.computeCosineSimilarity(jsonReq) 
    if algorithm == 'euclidean': id, simValue = evalu.computeEuclideanDist(jsonReq) 
    if algorithm == 'naive': id, simValue = evalu.computeNaiveDist(jsonReq) 

    #If alg param didn't match any of the previous, return error
    if id is None:
        raise errorHandler('Invalid alg parameter', statusCode=404)

    end= time.time()
    print(f'Tempo {algorithm}: {end-start}')
    #Else return response to the client
    return jsonify({'matches':[{'id':i} for i in id], 'metric':algorithm, 'value':round(simValue,3)})

@app.route('/profiles', methods=['DELETE'])
def deleteProfile():
    #Get request parameter representing the name/id of the loaded profile
    id = request.args.get('id', None)
    if id is None:
        raise errorHandler("Must give an ID parameter", statusCode=400)
    #Compose the filename + path
    filename = './computedFiles/'+id+'.json'

    if os.path.exists(filename):
        os.remove(filename)
    else:
        raise errorHandler("The specified profile does not exist", statusCode=404)

    #Apply a filter to evalu.targets to remove the deleted profile
    evalu.targets = list(filter(lambda p: p['id']!=id, evalu.targets))

    return jsonify({'message':'Profile removed correctly','id':id})

@app.route('/profiles/<id>', methods=['GET'])
def getProfile(id):

    #Compose the filename + path
    filename = './computedFiles/'+id+'.json'

    #Raise error if specified id does not exists
    if not os.path.exists(filename):
        raise errorHandler("The specified profile does not exist", statusCode=404)
        
    #Else, load the json data of the file
    jsonFile = open(filename)
    jsonStr = jsonFile.read()
    data = json.loads(jsonStr)

    #Return the json
    return jsonify({'id':id, 'data':data})

@app.route('/profiles', methods=['GET'])
def allProfiles():
    #Creating empty profile list
    profiles = []
    #For each file representing a profile
    for file in os.listdir('./computedFiles'):
        if file.endswith('.json'):
            #Add it to the list
            profiles.append({'id':file.split('.')[0]})

    #Return the list of profiles
    return jsonify(profiles)

@app.route('/profiles', methods=['POST'])
def addProfile():
    #Get request body
    jsonProf = request.get_json(silent=True)
    if jsonProf is None:
        raise errorHandler("No JSON gave", statusCode=400)

    #Get request parameter representing the name/id of the loaded profile
    id = request.args.get('id', None)
    if id is None:
        raise errorHandler("Must give an ID parameter", statusCode=500)
       
    #Compose the filename + path
    filename = './computedFiles/'+id+'.json'

    #Check if filename already exists
    if(os.path.exists(filename)):
        raise errorHandler("User ID already in use, choose another one", statusCode=409)

    with open(filename, 'w') as newJson:
        json.dump(jsonProf, newJson, separators=(',\n\t', ':'))


    #Add the new json profile to the evaluator

    evalu.targets.append({'id':id, 'data':jsonProf})

    #Return code 201 CREATED
    return jsonify({'message':'Profile added correctly','id':id}), 201



if __name__ == '__main__':
    #Default host = 127.0.0.1
    #Default port = 5000
    app.run()