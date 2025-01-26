import boto3
import json
import os
import requests

def handler(event, context):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('metaout')

    objects = []

    for obj in bucket.objects.all():
        objects.append(str(obj.key))

    print('Object Count: '+str(len(objects)))

    for obj in objects:
        local = obj.replace('/', '-')
        parse = obj.split('/')

        print(parse)


    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/sponsors/jblukach')
    }