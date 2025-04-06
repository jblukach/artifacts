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

    with zipfile.ZipFile('/tmp/amazon.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        with open('/tmp/amazon.csv', 'w') as f:
            f.write('sha256,fsize,fname,count\n')
            for obj in objects:
                if 'Amazon' in obj:
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
        zipf.write('/tmp/amazon.csv','amazon.csv')
    zipf.close()

    with zipfile.ZipFile('/tmp/apple.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        with open('/tmp/apple.csv', 'w') as f:
            f.write('sha256,fsize,fname,count\n')
            for obj in objects:
                if 'Apple' in obj:
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
        zipf.write('/tmp/apple.csv','apple.csv')
    zipf.close()

    with zipfile.ZipFile('/tmp/microsoft.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        with open('/tmp/microsoft.csv', 'w') as f:
            f.write('sha256,fsize,fname,count\n')
            for obj in objects:
                if 'Microsoft' in obj:
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
        zipf.write('/tmp/microsoft.csv','microsoft.csv')
    zipf.close()

    with zipfile.ZipFile('/tmp/ubuntu.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        with open('/tmp/ubuntu.csv', 'w') as f:
            f.write('sha256,fsize,fname,count\n')
            for obj in objects:
                if 'Ubuntu' in obj:
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
        zipf.write('/tmp/ubuntu.csv','ubuntu.csv')
    zipf.close()

    blake3 = list(set(blake3))
    b3lols = list(set(b3lols))

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
    s3client.upload_file('/tmp/amazon.csv', 'tempmeta', 'amazon.csv')
    s3client.upload_file('/tmp/apple.csv', 'tempmeta', 'apple.csv')
    s3client.upload_file('/tmp/microsoft.csv', 'tempmeta', 'microsoft.csv')
    s3client.upload_file('/tmp/ubuntu.csv', 'tempmeta', 'ubuntu.csv')
    

    sha256amazon = sha256sum('/tmp/amazon.zip')
    sha256apple = sha256sum('/tmp/apple.zip')
    sha256microsoft = sha256sum('/tmp/microsoft.zip')
    sha256ubuntu = sha256sum('/tmp/ubuntu.zip')

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
        "body":"### SHA256\\n\\n- **Amazon**: '''+sha256amazon+'''\\n- **Apple**: '''+sha256apple+'''\\n- **Microsoft**: '''+sha256microsoft+'''\\n- **Ubuntu**: '''+sha256ubuntu+'''",
        "draft":false,
        "prerelease":false,
        "generate_release_notes":false
    }'''

    response = requests.post(
        'https://api.github.com/repos/4n6ir/artifacts/releases',
        headers=headers,
        data=data
    )

    tagged = response.json()['id']
    print(response.json())

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"amazon.zip"
    }

    url = 'https://uploads.github.com/repos/4n6ir/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/amazon.zip', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"apple.zip"
    }

    url = 'https://uploads.github.com/repos/4n6ir/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/apple.zip', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"microsoft.zip"
    }

    url = 'https://uploads.github.com/repos/4n6ir/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/microsoft.zip', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"ubuntu.zip"
    }

    url = 'https://uploads.github.com/repos/4n6ir/artifacts/releases/'+str(tagged)+'/assets'

    with open('/tmp/ubuntu.zip', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/sponsors/jblukach')
    }