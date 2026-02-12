import boto3
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def handler(event, context):

    r = requests.get('https://www.loobins.io/loobins.json')

    if r.status_code == 200:

        loobins = []

        for entry in r.json():
            loobins.append(entry['name'])

        print('LOOBins: '+str(len(loobins)))

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['LOOBINS_TABLE'])

        response = table.query(
            KeyConditionExpression = Key('pk').eq('LOO#')
        )
        responsedata = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.query(
                KeyConditionExpression = Key('pk').eq('LOO#'),
                ExclusiveStartKey = response['LastEvaluatedKey']
            )
            responsedata.update(response['Items'])

        print('DynamoDB: '+str(len(responsedata)))

        for entry in loobins:

            if entry not in responsedata:

                table.put_item(
                    Item = {
                        'pk': 'LOO#',
                        'sk': entry
                    }
                )

        for entry in responsedata:

            if entry['sk'] not in loobins:

                table.delete_item(
                    Key = {
                        'pk': 'LOO#',
                        'sk': entry['sk']
                    }
                )

    return {
        'statusCode': 200,
        'body': json.dumps('https://www.loobins.io')
    }