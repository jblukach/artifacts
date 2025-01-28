import boto3
import datetime
import json
import os
import requests

def handler(event, context):

    s3client = boto3.client('s3')

    s3client.download_file('tempmeta  ', 'verification.csv', '/tmp/verification.csv')



    return {
        'statusCode': 200,
        'body': json.dumps('https://4n6ir.com')
    }