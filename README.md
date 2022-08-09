# AWS SSB 자가진단 애플리케이션

본 문서에서는 [SSB Application](https://github.com/kyoonkwon/SSB)에 사용된 lambda 함수들의 구현 로직과 코드, Step Functions를 이용한 플로우 개선에 대해 안내합니다.

- - - 

<img width="812" alt="image" src="https://user-images.githubusercontent.com/61778930/183718584-f193dbc9-8cd5-4929-8c80-43726af87c68.png">

# AWS SSB 보안 진단

AWS SSB 보안 사항을 진단하는 함수는 API에 접속하면 자동으로 실행됩니다. 혹은 배포된 이후에 Lambda 함수를 통하여 직접 실행하는 것도 가능합니다.

보안 진단은 AWS SSB에서 가이드 하는 항목 중 계정 보안을 중심으로 진단합니다. 진단하는 항목은 크게 4가지 항목으로 나뉩니다.

1. Account 및 IAM 설정
2. CloudTrail 설정
3. S3 설정
4. EC2 global 설정, Alarm, Trusted Advisor, GaurdDuty 등 기타 설정

**[1. Account 및 IAM 설정](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR/1-introduction/diagnose#1.-account-iam)**

이 항목에서는 계정 정보와 루트 계정을 포함한 IAM 설정에 대하여 진단합니다.

- 대체 연락처 정보가 기입되어 있는지
- 루트 유저에 MFA 설정 등의 설정이 되어있는지
- IAM User를 사용하는지
- IAM User에 직접 권한을 할당하여 사용하는지

**[2. CloudTrail 설정](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR/1-introduction/diagnose#2.-cloudtrail)**

이 항목에서는 아래 CloudTrail 설정에 대하여 진단합니다.

- CloudTrail이 켜져 있는지
- CloudTrail이 multi-region으로 되어있는지

**[3. S3 설정](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR/1-introduction/diagnose#3.-s3)**

이 항목에서는 S3 버킷의 퍼블릭 엑세스 정책에 대하여 진단합니다.

- 계정의 S3 퍼블릭 엑세스 정책이 차단되어있는지
- 개별 S3 버킷의 퍼블릭 엑세스가 차단되어있는지

**[4. 기타 설정](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR/1-introduction/diagnose#4.)**

이 항목에서는 나머지 AWS SSB 항목에 대하여 진단합니다.

- VPC, Subnet, Securit Group 체크
- 비용 및 루트 계정 엑세스 알람 설정
- Trusted Advisor 기능
- GuardDuty 기능

위 과정을 통해 진단된 결과는 `html` 형식의 리포트로 s3 버킷에 저장됩니다.


<img width="790" alt="image" src="https://user-images.githubusercontent.com/61778930/183718842-eb098f8e-3af7-48ae-819b-4b387870083b.png">

- - -
# 기존 Architecture

<img width="1304" alt="image" src="https://user-images.githubusercontent.com/61778930/183722517-b3e8e43f-8593-4a81-8f79-2a7ee5c528b2.png">

### Pain Points
1. 실행 시간: 병렬화를 위한 10개의 thread 실행으로 인해, 메모리를 많이 점유하여 실행 시간이 오래 걸립니다. 
2. 비용: 메모리 할당량을 늘려 속도를 개선할 수 있지만, 애플리케이션 실행 중 lambda를 작동하는 데에 비용이 늘어나게 됩니다. 
3. 불필요한 상태 관리 코드: 오류 처리 및 조건 관리와 같은 작업 상태 관리 코드가 길어져 핵심 로직을 알아보기 어렵고 유지보수에 비효율적입니다.

- - - 

# Step Functions를 이용한 플로우 개선 

## Architecture
<img width="1201" alt="image" src="https://user-images.githubusercontent.com/61778930/183723902-cdd2552f-e8bb-42a2-97bf-0de1526f0a8b.png">

## State Machine 구성
![stepfunctions_graph (14)](https://user-images.githubusercontent.com/61778930/183724171-fbbe33db-fb8d-409d-b3e4-c270153f3afc.png)

### 주요 개선 사항
1. 

## Proof of Concept
### 1. 실행 시간 관점


### 2. 비용 관점


## Workshop

애플리케이션의 내용과 사용 방법에 대한 자세한 안내는 [Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR)을 참고해주세요. 

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
