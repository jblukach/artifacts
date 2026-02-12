import boto3
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def handler(event, context):

    r = requests.get('https://lolbas-project.github.io/api/lolbas.json')

    if r.status_code == 200:

        lolbas = []

        for entry in r.json():
            lolbas.append(entry['Name'])

        print('LOLBAS: '+str(len(lolbas)))

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['LOLBAS_TABLE'])

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

        print('DynamoDB: '+str(len(responsedata)))

        for entry in lolbas:

            if entry not in responsedata:

                table.put_item(
                    Item = {
                        'pk': 'LOL#',
                        'sk': entry
                    }
                )

        for entry in responsedata:

            if entry['sk'] not in lolbas:

                table.delete_item(
                    Key = {
                        'pk': 'LOL#',
                        'sk': entry['sk']
                    }
                )

    return {
        'statusCode': 200,
        'body': json.dumps('https://lolbas-project.github.io/api')
    }