import boto3
from datetime import date, datetime, timedelta, timezone
import json
import report
import os

def lambda_handler(event, context):
    sts = boto3.client("sts")
    #resource = boto3.resource('s3')
    bucket = os.environ["Bucket"][13:]
    #bucketob = resource.Bucket(os.environ["Bucket"][13:])
    s3 = boto3.client('s3', config=boto3.session.Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
    sns= boto3.client("sns")
    topic = os.environ["Topic"]
        
    ###### HTML 생성 ###### 
    obj_A = s3.get_object(Bucket=bucket, Key=f'result-A-{date.today().isoformat()}.json')
    #bucketob.Object(f'result-A-{date.today().isoformat()}.json').get()
    obj_B = s3.get_object(Bucket=bucket, Key=f'result-B-{date.today().isoformat()}.json')
    obj_C = s3.get_object(Bucket=bucket, Key=f'result-C-{date.today().isoformat()}.json')
    obj_D = s3.get_object(Bucket=bucket, Key=f'result-D-{date.today().isoformat()}.json')
        
    # A,B,C,D 파일 읽어오고 
    results_A = json.loads(obj_A["Body"].read().decode('utf-8'))
    results_B = json.loads(obj_B["Body"].read().decode('utf-8'))
    results_C = json.loads(obj_C["Body"].read().decode('utf-8'))
    results_D = json.loads(obj_D["Body"].read().decode('utf-8'))
    
    ## 배열 results에 인덱스로 추가
    results = []
    allLambdaResult=[results_A, results_B, results_C, results_D];
    for eachLambdaResult in allLambdaResult:
        for r in eachLambdaResult:
            results.append(r)
            
    results.sort(key=lambda x: x["title"])
    account = sts.get_caller_identity()["Account"]
    html = report.generate_report(account, results)
    object_name = f"result-{date.today().isoformat()}.html"
    
    ###### HTML S3 업로드 ######
    try:
        encoded = bytes(html.encode('UTF-8'))
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket, Key=object_name, Body=encoded)
        
        presigned = int(os.environ["Presigned"])
    
        try:
            response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': object_name},
                                                    ExpiresIn=presigned * 60 * 60)        
            
            KST = timezone(timedelta(hours=9))
            expired = datetime.now(tz=KST) + timedelta(hours=presigned)
    
            sns.publish(TopicArn=topic, Message=f"""        
            리포트 파일의 미리 서명된(pre-signed) url을 생성하였습니다.
            {expired.isoformat()} 까지 다운로드가 가능합니다.
            url이 길어서 일부만 링크되었을 수 있습니다. 그럴 경우, 아래 링크를 전부 복사하여 접속해주세요.
            {response}
            """)
    
    
            return {
                'statusCode': 200,
                "body": "Success",
                "headers": {
                    'Content-Type': 'text/html',
                }
            }
            
        except Exception as e:
    
            sns.publish(TopicArn=topic, Message=f"""        
            리포트를 불러오는 중 오류가 발생하였습니다.
            {e}
            """)
    
            return {
                'statusCode': 400,
                "body": "Failed",
                "headers": {
                    'Content-Type': 'text/html',
                }
            }
        
    except Exception as e:
        sns.publish(TopicArn=topic, Message=f"""        
               리포트를 s3 버킷에 업로드 중 오류가 발생하였습니다.
                {e}
        """)

        return {
            'statusCode': 400,
            'body': f"upload fail\n {e}",
            "headers": {
                'Content-Type': 'text/html',
            }
        }
    
def upload_file(bucket, name, file):
    encoded = bytes(file.encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=name, Body=encoded)
        return True
    except:
        return False
