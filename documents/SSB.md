# SSB Application

본 문서에서는 AWS Startup 계정 보안 진단 도구 SSB Application에 대하여 안내합니다.

- [SSB Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR)
- [SSB Application code](https://github.com/kyoonkwon/SSB)

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
