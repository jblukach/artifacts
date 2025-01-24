import boto3
import json
from boto3.dynamodb.conditions import Key

athena = boto3.client('athena')
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
    table = event['name'].lower()

    if event['category'] == 'b3hash':

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3hash), COUNT(b3hash) AS total FROM matchmeta."+table+" WHERE b3hash != 'DENIED' AND b3hash != 'EMPTY' AND b3hash != 'ERROR' AND b3hash != 'LARGE' AND b3hash != 'ZERO' GROUP BY b3hash ORDER BY b3hash ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

    elif event['category'] == 'b3name':

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3name), COUNT(b3name) AS total FROM matchmeta."+table+" WHERE b3name != 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262' GROUP BY b3name ORDER BY b3name ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

    elif event['category'] == 'b3path':

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3path), COUNT(b3path) AS total FROM matchmeta."+table+" WHERE b3path != 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262' GROUP BY b3path ORDER BY b3path ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

    elif event['category'] == 'b3dir':

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3dir), COUNT(b3dir) AS total FROM matchmeta."+table+" WHERE b3dir != 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262' GROUP BY b3dir ORDER BY b3dir ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

    elif event['category'] == 'b3lol':

        if 'Microsoft' in event['name']:
            lols = lolbas()
        else:
            lols = gtfobins()

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3hash), COUNT(b3hash) AS total FROM matchmeta."+table+" WHERE LOWER(fname) IN ("+lols+") AND b3hash != 'DENIED' AND b3hash != 'EMPTY' AND b3hash != 'ERROR' AND b3hash != 'LARGE' AND b3hash != 'ZERO' GROUP BY b3hash ORDER BY b3hash ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/b3hash/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3name), COUNT(b3name) AS total FROM matchmeta."+table+" WHERE LOWER(fname) IN ("+lols+") AND b3name != 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262' GROUP BY b3name ORDER BY b3name ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/b3name/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

        response = athena.start_query_execution(
            QueryString = "UNLOAD (SELECT DISTINCT(b3path), COUNT(b3path) AS total FROM matchmeta."+table+" WHERE LOWER(fname) IN ("+lols+") AND b3path != 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262' GROUP BY b3path ORDER BY b3path ASC) TO 's3://metaout/"+event['name']+"/"+event['category']+"/b3path/' WITH (format = 'TEXTFILE', compression = 'NONE', field_delimiter = ',')",
            ResultConfiguration = {
                'OutputLocation': 's3://tempmeta/temp/'
            }
        )

        print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Search & Export')
    }