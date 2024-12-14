#!/usr/bin/env python3

import boto3
import json
from flask import Flask, jsonify, Response
from boto3.dynamodb.conditions import Attr
import numpy as np

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('proy-stats')

@app.route('/maxdiff')
def maxdiff():
    yearmonth = request.args.get('YearMonth') 

    response = table.query(
        FilterExpression=Attr('YearMonth').eq(yearmonth)
    )

    if reponse.get("Items") is None:
        Response("{'a':'b'}", status=404, mimetype='application/json')
    else:
        temperatures_mean = [t['Mean'] for t in response['Items']]

    return jsonify(max(temperatures_mean) - min(temperatures_mean))

@app.route('/sd')
def sd():
    yearmonth = request.args.get('YearMonth') 

    response = table.query(
        FilterExpression=Attr('YearMonth').eq(yearmonth)
    )

    if reponse.get("Items") is None:
        Response("{'a':'b'}", status=404, mimetype='application/json')
    else:
        temperatures_Deviation = [t['Deviation'] for t in response]
    

    Deviation = max(temperatures_Deviation)

    return jsonify(Deviation)

@app.route('/temp'):
def temp():
    yearmonth = request.args.get('YearMonth') 

    response = table.query(
        FilterExpression=Attr('YearMonth').eq(yearmonth)
    )

    if reponse.get("Items") is None:
        Response("{'a':'b'}", status=404, mimetype='application/json')
    else:
        temperatures_mean = [t['Mean'] for t in response]

    

    return np.mean(temperatures_mean)


if __name__ == '__main__':)
    app.run(debug=True, host='0.0.0.0', port=5000)

