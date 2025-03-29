import boto3
import datetime
import hashlib
import json
import os
import requests

def sha256sum(local):
    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()
    with open(local, 'rb') as h:
        buf = h.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = h.read(BLOCKSIZE)
    h.close()
    sha256 = sha256_hasher.hexdigest()
    return sha256

def handler(event, context):

    s3client = boto3.client('s3')

    s3client.download_file('matchmeta', '_binary/poppy-al23-arm', '/tmp/poppy')
    s3client.download_file('tempmeta', 'blake3.csv', '/tmp/blake3.csv')
    s3client.download_file('tempmeta', 'b3lols.csv', '/tmp/b3lols.csv')

    os.system('chmod +x /tmp/poppy')
    os.system('/tmp/poppy create -c 20000000 -p 0.001 /tmp/mmi.poppy')
    os.system('/tmp/poppy create -c 200000 -p 0.001 /tmp/lol.poppy')
    os.system('/tmp/poppy insert /tmp/mmi.poppy /tmp/blake3.csv')
    os.system('/tmp/poppy insert /tmp/lol.poppy /tmp/b3lols.csv')
    os.system('/tmp/poppy show /tmp/mmi.poppy')
    os.system('/tmp/poppy show /tmp/lol.poppy')

    with open('/tmp/verification.csv', 'w') as f:
        f.write('sha256,fname\n')
        sha256 = sha256sum('/tmp/mmi.poppy')
        f.write(sha256+',mmi.poppy\n')
        sha256 = sha256sum('/tmp/lol.poppy')
        f.write(sha256+',lol.poppy\n')
    f.close()

    ssm = boto3.client('ssm')

    token = ssm.get_parameter(
        Name = '/github/jblukach/releases', 
        WithDecryption = True
    )

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28'
    }

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    data = '''{
        "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(day)+'''",
        "target_commitish":"main",
        "name":"artifacts",
        "body":"bloom filter: https://github.com/hashlookup/poppy",
        "draft":false,
        "prerelease":false,
        "generate_release_notes":false
    }'''

    response = requests.post(
        'https://api.github.com/repos/jblukach/artifacts/releases',
        headers=headers,
        data=data
    )

    tagged = response.json()['id']
    print(response.json())

    ### mmi.poppy ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"mmi.poppy"
    }

    url = 'https://uploads.github.com/repos/jblukach/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/mmi.poppy', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    ### lol.poppy ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"lol.poppy"
    }

    url = 'https://uploads.github.com/repos/jblukach/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/lol.poppy', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    ### verification.csv ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"verification.csv"
    }

    url = 'https://uploads.github.com/repos/jblukach/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/verification.csv', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/hashlookup/poppy')
    }