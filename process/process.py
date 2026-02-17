import boto3
import json

def handler(event, context):

    s3client = boto3.client('s3')
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket('matchmetaoutput')

    objects = []

    for obj in bucket.objects.all():
        objects.append(str(obj.key))

    print('Object Count: '+str(len(objects)))

    amazonb3s = []
    amazonlols = []

    for obj in objects:
        if 'amazon' in obj:
            local = obj.replace('/', '-')
            s3client.download_file('matchmetaoutput', obj, '/tmp/'+local+'.csv')
            with open('/tmp/'+local+'.csv', 'r') as r:
                for line in r:
                    line = line.split(',')
                    amazonb3s.append(line[0])
                    if 'b3lol' in local:
                        amazonlols.append(line[0])
            r.close()

    print('amazonb3s: '+str(len(amazonb3s)))
    amazonb3s = list(set(amazonb3s))
    print('amazonb3s: '+str(len(amazonb3s)))
    print('amazonlols: '+str(len(amazonlols)))
    amazonlols = list(set(amazonlols))
    print('amazonlols: '+str(len(amazonlols)))

    with open('/tmp/amazon.csv', 'w') as f:
        for b3 in amazonb3s:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/amazon-lols.csv', 'w') as f:
        for b3 in amazonlols:
            f.write(b3+'\n')
    f.close()

    s3client.upload_file('/tmp/amazon.csv', 'matchmetastaged', 'amazon.csv')
    s3client.upload_file('/tmp/amazon-lols.csv', 'matchmetastaged', 'amazon-lols.csv')

    macosb3s = []
    macoslols = []

    for obj in objects:
        if 'macos' in obj:
            local = obj.replace('/', '-')
            s3client.download_file('matchmetaoutput', obj, '/tmp/'+local+'.csv')
            with open('/tmp/'+local+'.csv', 'r') as r:
                for line in r:
                    line = line.split(',')
                    macosb3s.append(line[0])
                    if 'b3lol' in local:
                        macoslols.append(line[0])
            r.close()

    print('macosb3s: '+str(len(macosb3s)))
    macosb3s = list(set(macosb3s))
    print('macosb3s: '+str(len(macosb3s)))
    print('macoslols: '+str(len(macoslols)))
    macoslols = list(set(macoslols))
    print('macoslols: '+str(len(macoslols)))

    with open('/tmp/macos.csv', 'w') as f:
        for b3 in macosb3s:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/macos-lols.csv', 'w') as f:
        for b3 in macoslols:
            f.write(b3+'\n')
    f.close()

    s3client.upload_file('/tmp/macos.csv', 'matchmetastaged', 'macos.csv')
    s3client.upload_file('/tmp/macos-lols.csv', 'matchmetastaged', 'macos-lols.csv')

    ubuntub3s = []
    ubuntulols = []

    for obj in objects:
        if 'ubuntu' in obj:
            local = obj.replace('/', '-')
            s3client.download_file('matchmetaoutput', obj, '/tmp/'+local+'.csv')
            with open('/tmp/'+local+'.csv', 'r') as r:
                for line in r:
                    line = line.split(',')
                    ubuntub3s.append(line[0])
                    if 'b3lol' in local:
                        ubuntulols.append(line[0])
            r.close()

    print('ubuntub3s: '+str(len(ubuntub3s)))
    ubuntub3s = list(set(ubuntub3s))
    print('ubuntub3s: '+str(len(ubuntub3s)))
    print('ubuntulols: '+str(len(ubuntulols)))
    ubuntulols = list(set(ubuntulols))
    print('ubuntulols: '+str(len(ubuntulols)))

    with open('/tmp/ubuntu.csv', 'w') as f:
        for b3 in ubuntub3s:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/ubuntu-lols.csv', 'w') as f:
        for b3 in ubuntulols:
            f.write(b3+'\n')
    f.close()

    s3client.upload_file('/tmp/ubuntu.csv', 'matchmetastaged', 'ubuntu.csv')
    s3client.upload_file('/tmp/ubuntu-lols.csv', 'matchmetastaged', 'ubuntu-lols.csv')

    windowsb3s = []
    windowslols = []

    for obj in objects:
        if 'windows' in obj:
            local = obj.replace('/', '-')
            s3client.download_file('matchmetaoutput', obj, '/tmp/'+local+'.csv')
            with open('/tmp/'+local+'.csv', 'r') as r:
                for line in r:
                    line = line.split(',')
                    windowsb3s.append(line[0])
                    if 'b3lol' in local:
                        windowslols.append(line[0])
            r.close()

    print('windowsb3s: '+str(len(windowsb3s)))
    windowsb3s = list(set(windowsb3s))
    print('windowsb3s: '+str(len(windowsb3s)))
    print('windowslols: '+str(len(windowslols)))
    windowslols = list(set(windowslols))
    print('windowslols: '+str(len(windowslols)))

    with open('/tmp/windows.csv', 'w') as f:
        for b3 in windowsb3s:
            f.write(b3+'\n')
    f.close()

    with open('/tmp/windows-lols.csv', 'w') as f:
        for b3 in windowslols:
            f.write(b3+'\n')
    f.close()

    s3client.upload_file('/tmp/windows.csv', 'matchmetastaged', 'windows.csv')
    s3client.upload_file('/tmp/windows-lols.csv', 'matchmetastaged', 'windows-lols.csv')

    return {
        'statusCode': 200,
        'body': json.dumps('https://github.com/sponsors/jblukach')
    }