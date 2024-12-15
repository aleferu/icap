#!/usr/bin/env python3

import boto3
from flask import Flask, Response, request
from boto3.dynamodb.conditions import Key
import statistics

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('proy-stats')

def get_yearmonth():
    month, year = request.args.get('month'), request.args.get('year')
    try:
        month = int(month)
        year = int(year)
    except (ValueError, TypeError):
        return None
    return year * 100 + month

def build_json_response(msg, status):
    return Response(msg, status=status, mimetype='application/json')

def build_ok_json_response(msg):
    return build_json_response(msg, 200)

def get_invalid_args_response():
    http_code = 400  # Bad Request
    response_json = {
        'error': 'Invalid arguments. Make sure \'month\' and \'year\' are provided and are valid.'
    }
    return build_json_response(str(response_json), http_code)

def get_not_found_response():
    http_code = 404  # Not Found
    response_json = {
        'error': 'Combination of month and year not found in DB.'
    }
    return build_json_response(str(response_json), http_code)

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
    return build_ok_json_response(str(result))

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
    return build_ok_json_response(str(result))

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
    return build_ok_json_response(str(result))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
