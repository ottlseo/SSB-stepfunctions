import boto3
import ssb
import datetime
import json
import os

def lambda_handler(event, context):
    session = boto3.Session()
    bucket = os.environ['Bucket'][13:]

    try:
        results = ssb.checks(session)
        name = f"result-B-{datetime.date.today().isoformat()}.json"
        
        if upload_file(bucket, name, json.dumps(results)):
            return {
            'statusCode': 200,
            "body": json.dumps("upload success"),
            }
        else:
            return {
            'statusCode': 400,
            'body': json.dumps("upload fail")
            }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("upload fail")
            }
    
def upload_file(bucket, name, file):
    encoded = bytes(file.encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=name, Body=encoded)
        return True
    except:
        return False

if __name__ == "__main__":
    lambda_handler(None, None)