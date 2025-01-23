import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def gtfobins():
    table = dynamodb.Table('gtfobins')
    response = table.query(
        KeyConditionExpression = Key('pk').eq('GTFO#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression = Key('pk').eq('GTFO#'),
            ExclusiveStartKey = response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])
    gtfobins = ''
    for item in responsedata:
        gtfobins = gtfobins+"'"+item['sk'].lower()+"',"
    gtfobins = gtfobins[:-1]
    return gtfobins

def lolbas():
    table = dynamodb.Table('lolbas')
    response = table.query(
        KeyConditionExpression = Key('pk').eq('LOL#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression = Key('pk').eq('LOL#'),
            ExclusiveStartKey = response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])
    lolbas = ''
    for item in responsedata:
        lolbas = lolbas+"'"+item['sk'].lower()+"',"
    lolbas = lolbas[:-1]
    return lolbas

def handler(event, context):

    print(event)
    event = {}
    event['name'] = 'search'
    print(event)

    athena = boto3.client('athena')


    return {
        'statusCode': 200,
        'body': json.dumps('Search & Export')
    }