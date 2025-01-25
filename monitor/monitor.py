import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):

    athena = boto3.client('athena')
    topic = boto3.client('sns')

    paginator = athena.get_paginator('list_query_executions')
    pages = paginator.paginate(
        WorkGroup = 'primary'
    )

    queryids = []

    for page in pages:
        for query in page['QueryExecutionIds']:
            response = athena.get_query_execution(
                QueryExecutionId = query
            )
            if response['QueryExecution']['Status']['State'] == 'FAILED':
                queryids.append(response['QueryExecution']['QueryExecutionId'])
            
    print('Failed Queries: '+str(len(queryids)))

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['ATHEANA_TABLE'])

    response = table.query(
        KeyConditionExpression = Key('pk').eq('QUERY#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression = Key('pk').eq('QUERY#'),
            ExclusiveStartKey = response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    previousids = []
    for item in responsedata:
        previousids.append(item['sk'])

    print('DynamoDB: '+str(len(previousids)))

    for query in queryids:

        if query not in previousids:

            table.put_item(
                Item = {
                    'pk': 'QUERY#',
                    'sk': query
                }
            )

            topic.publish(
                TopicArn = os.environ['SNS_TOPIC'],
                Message = 'Query Failed: '+query
            )

    return {
        'statusCode': 200,
        'body': json.dumps('https://docs.aws.amazon.com/athena/latest/ug/monitor-with-cloudtrail.html')
    }