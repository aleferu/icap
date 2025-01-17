#!/usr/bin/env python3

import boto3
from flask import Flask, jsonify, request
from boto3.dynamodb.conditions import Key
import statistics

app = Flask(__name__)

# Conection to the DynamoBD resource and getting the corresponding table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('proy-stats')

# Gets the arguments of the request
def get_yearmonth():
    month, year = request.args.get('month'), request.args.get('year')
    try:
        month = int(month)
        year = int(year)
    except (ValueError, TypeError):
        return None
    return year * 100 + month

def build_json_response(dict_response, status):
    return jsonify(dict_response), status, {'Content-Type': 'application/json'}

# Default response for a well built request
def build_ok_json_response(dict_response):
    return build_json_response(dict_response, 200)

# Default response for a request with bad arguments
def get_invalid_args_response():
    http_code = 400  # Bad Request
    response_json = {
        'error': 'Invalid arguments. Make sure \'month\' and \'year\' are provided and are valid.'
    }
    return build_json_response(response_json, http_code)

# Response for a combination of month and year not found in DB.
def get_not_found_response():
    http_code = 404  # Not Found
    response_json = {
        'error': 'Combination of month and year not found in DB.'
    }
    return build_json_response(response_json, http_code)

# maxdiff endpoint
@app.route('/maxdiff')
def maxdiff():
    yearmonth = get_yearmonth()

    if yearmonth is None:
        return get_invalid_args_response()

    response = table.query(
        KeyConditionExpression=Key('YearMonth').eq(yearmonth)
    )

    items = response.get('Items', [])

    if len(items) == 0:
        return get_not_found_response()

    temperatures_mean = [t['Mean'] for t in items]
    result = {
        'result': max(temperatures_mean) - min(temperatures_mean)
    }
    return build_ok_json_response(result)

# sd endpoint
@app.route('/sd')
def sd():
    yearmonth = get_yearmonth()

    if yearmonth is None:
        return get_invalid_args_response()

    response = table.query(
        KeyConditionExpression=Key('YearMonth').eq(yearmonth)
    )

    items = response.get('Items', [])

    if len(items) == 0:
        return get_not_found_response()
    
    temperatures_deviation = [t['Deviation'] for t in items]
    result = {
        'result': max(temperatures_deviation)
    }
    return build_ok_json_response(result)

# temp endpoint
@app.route('/temp')
def temp():
    yearmonth = get_yearmonth()

    if yearmonth is None:
        return get_invalid_args_response()

    response = table.query(
        KeyConditionExpression=Key('YearMonth').eq(yearmonth)
    )

    items = response.get('Items', [])

    if len(items) == 0:
        return get_not_found_response()

    temperatures_mean = [t['Mean'] for t in items]
    result = {
        'result': statistics.mean(temperatures_mean)
    }
    return build_ok_json_response(result)

# endpoint to indicate to aws that all is well
@app.route('/health')
def health():
    result = {
      'status': 'UP',
      'message': 'Service is healthy'
    }
    return build_ok_json_response(result)

# Not valid URI
@app.errorhandler(404)
def page_not_found(_):
    http_code = 404  # Not Found
    response_json = {
        'error': 'URI is not valid. Options: /maxdiff , /sd , /temp'
    }
    return build_json_response(response_json, http_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
