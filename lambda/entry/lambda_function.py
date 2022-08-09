import boto3
from datetime import date, datetime, timezone, timedelta
import os

def lambda_handler(event, context):

    resource = boto3.resource('s3')
    bucket_name = os.environ["Bucket"][13:]
    bucket = resource.Bucket(bucket_name)
    lamb = boto3.client('lambda')

    sns = boto3.client("sns")
    topic = os.environ["Topic"]
    
    subscriptions = sns.list_subscriptions_by_topic(TopicArn = topic)["Subscriptions"]
    endpoints = list(map(lambda x: x["Endpoint"], subscriptions))

    # subscription 안 한 경우
    for sub in subscriptions:
        if sub["SubscriptionArn"] != "PendingConfirmation":
            break
    else:
        return {
            'statusCode': 400,
            "body": f"이메일로 발송된 topic을 먼저 subscribe 해주세요. {endpoints}",
            "headers": {
                'Content-Type': 'text/html;charset=UTF-8',
            }
        }

    flag = True
    last_modified = datetime.now(timezone.utc)
    try:
        last_modified = bucket.Object("temp").get()["LastModified"]
        if datetime.now(timezone.utc) - last_modified < timedelta(minutes=5):
            flag = False

    except Exception as e:
        print(e)
    
    return {
        'flag':flag
    }