import boto3
import json
import os
import requests
from bs4 import BeautifulSoup
from boto3.dynamodb.conditions import Key

def handler(event, context):

    r = requests.get('https://gtfobins.github.io/')

    if r.status_code == 200:

        soup = BeautifulSoup(r.text, 'html.parser')

        gtfobins = []

        for link in soup.find_all('a', class_='bin-name'):
            out = link.get('href').split('/')
            gtfobins.append(out[2])

        print('GTFOBins: '+str(len(gtfobins)))

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['GTFO_TABLE'])

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

        print('DynamoDB: '+str(len(responsedata)))

        for entry in gtfobins:

            if entry not in responsedata:

                table.put_item(
                    Item = {
                        'pk': 'GTFO#',
                        'sk': entry
                    }
                )

        for entry in responsedata:

            if entry['sk'] not in gtfobins:

                table.delete_item(
                    Key = {
                        'pk': 'GTFO#',
                        'sk': entry['sk']
                    }
                )

    return {
        'statusCode': 200,
        'body': json.dumps('https://gtfobins.github.io')
    }