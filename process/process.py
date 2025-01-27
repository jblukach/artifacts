import boto3
import datetime
import hashlib
import json
import os
import requests
import zipfile

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
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket('metaout')

    objects = []

    for obj in bucket.objects.all():
        objects.append(str(obj.key))

    print('Object Count: '+str(len(objects)))

    blake3 = []
    b3lols = []

    with zipfile.ZipFile('/tmp/artifacts.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        with open('/tmp/verification.csv', 'w') as f:
            f.write('sha256,fsize,fname,count\n')
            for obj in objects:
                local = obj.replace('/', '-')
                s3client.download_file('metaout', obj, '/tmp/'+local+'.csv')
                zipf.write('/tmp/'+local+'.csv',local+'.csv')
                fsize = os.path.getsize('/tmp/'+local+'.csv')
                sha256 = sha256sum('/tmp/'+local+'.csv')
                count = 0
                with open('/tmp/'+local+'.csv', 'r') as r:
                    for line in r:
                        count += 1
                        line = line.split(',')
                        blake3.append(line[0])
                        if 'b3lol' in local:
                            b3lols.append(line[0])
                r.close()
                f.write(sha256+','+str(fsize)+','+local+'.csv,'+str(count)+'\n')
            f.write(',,blake3 total,'+str(len(blake3))+'\n')
            blake3 = list(set(blake3))
            f.write(',,blake3 unique,'+str(len(blake3))+'\n')
            f.write(',,b3lols total,'+str(len(b3lols))+'\n')
            b3lols = list(set(b3lols))
            f.write(',,b3lols unique,'+str(len(b3lols))+'\n')
        f.close()
        zipf.write('/tmp/verification.csv','verification.csv')
    zipf.close()

    with open('/tmp/blake3.csv', 'w') as f:
        for b3 in blake3:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/b3lols.csv', 'w') as f:
        for b3 in b3lols:
            f.write(b3+'\n')
    f.close()

    s3client.upload_file('/tmp/blake3.csv', 'tempmeta', 'blake3.csv')
    s3client.upload_file('/tmp/b3lols.csv', 'tempmeta', 'b3lols.csv')
    s3client.upload_file('/tmp/verification.csv', 'tempmeta', 'verification.csv')

    sha256 = sha256sum('/tmp/artifacts.zip')

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

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    data = '''{
        "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(day)+'''",
        "target_commitish":"main",
        "name":"artifacts",
        "body":"sha256: '''+sha256+'''",
        "draft":false,
        "prerelease":false,
        "generate_release_notes":false
    }'''

    response = requests.post(
        'https://api.github.com/repos/4n6ir/artifacts/releases',
        headers=headers,
        data=data
    )

    print(response.json())

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"artifacts.zip"
    }

    url = 'https://uploads.github.com/repos/4n6ir/artifacts/releases/'+str(response.json()['id'])+'/assets'

    with open('/tmp/artifacts.zip', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/sponsors/jblukach')
    }