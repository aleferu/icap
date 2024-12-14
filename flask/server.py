#!/usr/bin/env python3

import boto3
import json
from flask import Flask, jsonify, Response
from boto3.dynamodb.conditions import Attr
import numpy as np

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('proy')

@app.route('/maxdiff')
def maxdiff():
    year = request.args.get('year')
    month = request.args.get('month') 

    response = table.scan(
        FilterExpression=Attr('year').eq(str(year)) & Attr('month').eq(str(month))
    )

    if response['Count'] == 0:
        Response("{'a':'b'}", status=404, mimetype='application/json')
    else:
        temperatures = [t['mean'] for t in response['Items']]

    return jsonify(max(temperatures) - min(temperatures))

@app.route('/sd')
def sd():
    year = request.args.get('year')
    month = request.args.get('month') 

    response = table.scan(
        FilterExpression=Attr('year').eq(str(year)) & Attr('month').eq(str(month))
    )['Items']

    temperatures = [t['sd'] for t in response]

    std = max(temperatures)

    return jsonify(std)

@app.route('/temp'):
def temp():
    year = request.args.get('year')
    month = request.args.get('month') 

    response = table.scan(
        FilterExpression=Attr('year').eq(str(year)) & Attr('month').eq(str(month))
    )

    temperatures = [t['mean'] for t in response]

    return np.mean(temperatures)


if __name__ == '__main__':)
    app.run(debug=True, host='0.0.0.0', port=5000)

