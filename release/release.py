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

    s3client.download_file('matchmetastaged', 'poppy-al2023-arm64', '/tmp/poppy')
    s3client.download_file('matchmetastaged', 'amazon.csv', '/tmp/amazon.csv')
    s3client.download_file('matchmetastaged', 'amazon-lols.csv', '/tmp/amazon-lols.csv')
    s3client.download_file('matchmetastaged', 'macos.csv', '/tmp/macos.csv')
    s3client.download_file('matchmetastaged', 'macos-lols.csv', '/tmp/macos-lols.csv')
    s3client.download_file('matchmetastaged', 'ubuntu.csv', '/tmp/ubuntu.csv')
    s3client.download_file('matchmetastaged', 'ubuntu-lols.csv', '/tmp/ubuntu-lols.csv')
    s3client.download_file('matchmetastaged', 'windows.csv', '/tmp/windows.csv')
    s3client.download_file('matchmetastaged', 'windows-lols.csv', '/tmp/windows-lols.csv')

    totalb3s = []
    totallols = []

    amazon = 0
    amazonlols = 0

    with open('/tmp/amazon.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totalb3s.append(line.strip())
            amazon += 1
    f.close()

    with open('/tmp/amazon-lols.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totallols.append(line.strip())
            amazonlols += 1
    f.close()

    macos = 0
    macoslols = 0

    with open('/tmp/macos.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totalb3s.append(line.strip())
            macos += 1
    f.close()

    with open('/tmp/macos-lols.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totallols.append(line.strip())
            macoslols += 1
    f.close()

    ubuntu = 0
    ubuntulols = 0

    with open('/tmp/ubuntu.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totalb3s.append(line.strip())
            ubuntu += 1
    f.close()

    with open('/tmp/ubuntu-lols.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totallols.append(line.strip())
            ubuntulols += 1
    f.close()

    windows = 0
    windowslols = 0

    with open('/tmp/windows.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totalb3s.append(line.strip())
            windows += 1
    f.close()

    with open('/tmp/windows-lols.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            totallols.append(line.strip())
            windowslols += 1
    f.close()

    print('totalb3s: '+str(len(totalb3s)))
    totalb3s = list(set(totalb3s))
    print('totalb3s: '+str(len(totalb3s)))
    print('totallols: '+str(len(totallols)))
    totallols = list(set(totallols))
    print('totallols: '+str(len(totallols)))

    countb3s = len(totalb3s)
    countlols = len(totallols)

    with open('/tmp/totalb3s.csv', 'w') as f:
        for b3 in totalb3s:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/totallols.csv', 'w') as f:
        for b3 in totallols:
            f.write(b3+'\n')
    f.close()

    os.system('chmod +x /tmp/poppy')
    os.system('/tmp/poppy create -c 30000000 -p 0.001 /tmp/mmi.poppy')
    os.system('/tmp/poppy create -c 200000 -p 0.001 /tmp/lol.poppy')
    os.system('/tmp/poppy insert /tmp/mmi.poppy /tmp/totalb3s.csv')
    os.system('/tmp/poppy insert /tmp/lol.poppy /tmp/totallols.csv')
    os.system('/tmp/poppy show /tmp/mmi.poppy')
    os.system('/tmp/poppy show /tmp/lol.poppy')

    with open('/tmp/verification.csv', 'w') as f:
        f.write('sha256,fname\n')
        sha256 = sha256sum('/tmp/mmi.poppy')
        f.write(sha256+',mmi.poppy\n')
        sha256 = sha256sum('/tmp/lol.poppy')
        f.write(sha256+',lol.poppy\n')
    f.close()

    secret = boto3.client('secretsmanager')

    getsecret = secret.get_secret_value(
        SecretId = os.environ['SECRET_MGR_ARN']
    )

    token = json.loads(getsecret['SecretString'])

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['github'],
        'X-GitHub-Api-Version': '2022-11-28'
    }

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    data = '''{
        "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(day)+'''",
        "target_commitish":"main",
        "name":"artifacts",
        "body":"### B3: '''+str(countb3s)+'''\\n\\n- **amazon:** '''+str(amazon)+'''\\n- **macos:** '''+str(macos)+'''\\n- **ubuntu:** '''+str(ubuntu)+'''\\n- **windows:** '''+str(windows)+'''\\n\\n### LOL: '''+str(countlols)+'''\\n\\n- **amazon:** '''+str(amazonlols)+'''\\n- **macos:** '''+str(macoslols)+'''\\n- **ubuntu:** '''+str(ubuntulols)+'''\\n- **windows:** '''+str(windowslols)+'''\\n\\n",
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
        'Authorization': 'Bearer '+token['github'],
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
        'Authorization': 'Bearer '+token['github'],
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
        'Authorization': 'Bearer '+token['github'],
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