import base64
import boto3
import datetime
import json
import requests

def handler(event, context):

    s3client = boto3.client('s3')

    s3client.download_file('tempmeta', 'verification.csv', '/tmp/verification.csv')

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    blogname = year+'-'+month+'-'+day+'-artifacts.md'

    with open('/tmp/'+blogname, 'w') as w:
        w.write('---\n')
        w.write('layout: post\n')
        w.write('title: \"Artifacts - BLAKE3\"\n')
        w.write('author: \"John Lukach\"\n')
        w.write('tags: artifacts blake3 gtfobins lolbas loobins poppy\n')
        w.write('---\n\n')
        w.write('[Artifacts](https://github.com/jblukach/artifacts) release of [BLAKE3](https://github.com/BLAKE3-team/BLAKE3) hashes categorized by operating systems into the content hash, directory, file name, full path, and living-off-the-land ([gtfobins](https://gtfobins.github.io), [lolbas](https://lolbas-project.github.io), & [loobins](https://www.loobins.io)) sets to create [poppy](https://github.com/hashlookup/poppy) blooms.\n\n')
        w.write('| type | total |\n')
        w.write('|-----|\n')
        with open('/tmp/verification.csv', 'r') as f:
            for line in f.readlines():
                if 'blake3 total' in line or 'blake3 unique' in line or 'b3lols total' in line or 'b3lols unique' in line:
                    line = line.split(',')
                    w.write('|'+line[2]+'|'+line[3][:-1]+'|\n')
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

    url = 'https://api.github.com/repos/4n6ir/4n6ir.com/contents/_posts/'+blogname

    with open('/tmp/'+blogname, 'r') as f:
        content = f.read()
    f.close()

    content = base64.b64encode(content.encode()).decode()

    data = {
        'message': blogname,
        'content': content
    }

    response = requests.put(url, headers=headers, json=data)
    print(response.json())

    return {
        'statusCode': 200,
        'body': json.dumps('https://4n6ir.com')
    }