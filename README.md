# SSB Self-Test App

## Workshop

애플리케이션의 내용과 사용 방법에 대한 자세한 안내는 워크샵을 참고해주세요. 워크샵 링크는 이후 업데이트 됩니다.

본 문서에서는 배포된 lambda 함수들의 구현 로직과 코드를 AWS Severless Application Repository에 package/publish하는 방법에 대하여 안내합니다.

## Requirement

- AWS Account 및 배포에 필요한 권한을 가진 IAM User
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 설치 및 구성
- [AWS Serverless Application Model](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (AWS SAM)

## Package & Publish

### Package

Package는 작성한 코드, README, 라이센스 파일 등을 AWS S3에 업로드하고, yaml 형식의 template 파일을 CloudFormation 용 yaml 파일로 변환하는 과정입니다.

새로 publish를 하는 경우가 아니라 기존 애플리케이션을 업데이트하는 경우에는 `template.yaml`에서 Metadata의 SemanticVersion을 변경해주세요.

또한, 아래 package가 되지 않을 경우 명령어에 `--force-upload`를 추가해주세요

```
sam package \
 --template-file template.yaml \
 --output-template-file packaged.yaml \
 --s3-bucket {S3 bucket name} \
```

또한, S3 버킷의 리소스 정책에 아래 내용을 추가해주어야 Serverless Application Repository를 통하여 퍼블릭하게 배포가 가능합니다.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "serverlessrepo.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{bucket_name}/*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": {accountID}
                }
            }
        }
    ]
}
```

### Publish

Serverless Application Repository에 배포하는 방법입니다. 아래 명령어를 통하여 배포가 가능하며, `--region ap-northeast-2`와 같은 방식으로 배포 리전을 특정할 수 있습니다.

```
sam publish --template packaged.yaml
```

또는, Serverless Application Repository의 [내 애플리케이션](https://ap-northeast-2.console.aws.amazon.com/serverlessrepo/home?region=ap-northeast-2#/published-applications)에서 packaged.yaml 파일을 콘솔을 통하여 업로드하여 publish도 가능합니다.

## How it works

### entry

생성된 API Endpoint로 접속할 경우, `entry`의 `lambda_function`이 실행됩니다.
위 함수에서, 
1. email subscription이 존재하는지 확인
2. s3 버킷에 temp 파일의 최종 수정 시간을 통하여 마지막 API 호출로부터 5분이상 경과했는지 확인
3. ssb function을 호출 후, temp 파일 업데이트

를 수행합니다.


### ssb


### report