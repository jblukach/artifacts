import base64
import boto3
import datetime
import json
import requests

def handler(event, context):

    s3client = boto3.client('s3')

    s3client.download_file('tempmeta', 'amazon.csv', '/tmp/amazon.csv')
    s3client.download_file('tempmeta', 'apple.csv', '/tmp/apple.csv')
    s3client.download_file('tempmeta', 'microsoft.csv', '/tmp/microsoft.csv')
    s3client.download_file('tempmeta', 'rhel.csv', '/tmp/rhel.csv')
    s3client.download_file('tempmeta', 'suse.csv', '/tmp/suse.csv')
    s3client.download_file('tempmeta', 'ubuntu.csv', '/tmp/ubuntu.csv')

    with open('/tmp/README.md', 'w') as w:
        w.write('# artifacts')
        w.write('\n\n## Amazon Linux\n\n')
        with open('/tmp/amazon.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        w.write('\n\n## Apple macOS\n\n')
        with open('/tmp/apple.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        w.write('\n\n## Microsoft Windows\n\n')
        with open('/tmp/microsoft.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        w.write('\n\n## Red Hat Linux\n\n')
        with open('/tmp/rhel.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        w.write('\n\n## SUSE Linux\n\n')
        with open('/tmp/suse.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        w.write('\n\n## Ubuntu Linux\n\n')
        with open('/tmp/ubuntu.csv', 'r') as f:
            line = f.readline()
            line = line.split(',')
            w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
            w.write('|:---:|:---:|:---:|:---:|\n')
            for line in f.readlines():
                line = line.split(',')
                w.write('|'+line[0]+'|'+line[1]+'|'+line[2]+'|'+line[3][:-1]+'|\n')
        f.close()
    w.close()

    ssm = boto3.client('ssm')

    token = ssm.get_parameter(
        Name = '/github/4n6ir/release', 
        WithDecryption = True
    )

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28'
    }

    url = 'https://api.github.com/repos/4n6ir/artifacts/contents/README.md'

    response = requests.get(url, headers=headers)
    sha = response.json()['sha']
    print(response.json())

    url = 'https://api.github.com/repos/4n6ir/artifacts/contents/README.md'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28'
    }

    with open('/tmp/README.md', 'r') as f:
        content = f.read()
    f.close()

    content = base64.b64encode(content.encode()).decode()

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    data = {
        'message': 'artifacts '+str(year)+'.'+str(month)+'.'+str(day),
        'content': content,
        'sha': sha
    }

    response = requests.put(url, headers=headers, json=data)
    print(response.json())

    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/4n6ir/artifacts')
    }