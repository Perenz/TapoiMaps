import flask
import os
from flask import jsonify, Flask, request, make_response
import sys
import pandas as pd
sys.path.append('C:/Users/stefa/Desktop/U-Hopper/TapoiMaps')
import logic.Evaluator
from logic import Evaluator

app = flask.Flask(__name__)
app.config['DEBUG'] = True

match = {
    'file':'json',
    'name':'Roger',
    'date':'15',
    'ex':'work'
}

evalu = Evaluator.similarityEvaluator()


#Use a class where define the simEvaluator
#There, in the init i can load the files

@app.route('/', methods=['GET', 'POST'])
@app.route('/cosine', methods=['GET', 'POST'])
def cosine():
    json = request.get_json(silent=True)
    id, simValue = evalu.computeCosineSimilarity(pd.DataFrame(json, index=['test'])) 
    return jsonify({'id':id, 'value':simValue})

@app.route('/euclidean', methods=['GET', 'POST'])
def euclidean():
    json = request.get_json(silent=True)
    id, simValue = evalu.computeEuclideanDist(pd.DataFrame(json, index=['test'])) 
    return jsonify({'id':id, 'value':simValue})

app.run()