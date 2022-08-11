# AWS SSB 자가진단 애플리케이션

본 문서에서는 [SSB Application](https://github.com/kyoonkwon/SSB)에 사용된 lambda 함수들의 구현 로직과 코드, **Step Functions를 이용한 플로우 개선**에 대해 안내합니다.

### 👉 [SSB 애플리케이션이 더 궁금하다면?](./documents/SSB.md)

![image](https://user-images.githubusercontent.com/61778930/183725645-6980355f-e85b-4444-ae3a-dc35d5758c57.png)

- - -
# 기존 SSB의 Architecture

<img width="1304" alt="image" src="https://user-images.githubusercontent.com/61778930/183722517-b3e8e43f-8593-4a81-8f79-2a7ee5c528b2.png">

### Pain Points
위와 같은 아키텍처에서, 1개의 Lambda 내에서 10개의 thread를 생성하고 실행시켜 병렬 로직을 구현했습니다.   
이때 아래와 같은 문제점이 관찰되었습니다.

1. 실행 시간: 병렬화를 위한 10개의 thread 실행으로 인해, 메모리를 많이 점유하여 실행 시간이 오래 걸립니다. 
2. 비용: 메모리 할당량을 늘려 속도를 개선할 수 있지만, 애플리케이션 실행 중 lambda를 작동하는 데에 비용이 늘어나게 됩니다. 
3. 불필요한 상태 관리 코드: 오류 처리 및 조건 관리와 같은 작업 상태 관리 코드가 길어져 핵심 로직을 알아보기 어렵고 유지보수에 비효율적입니다.

- - - 

# Step Functions를 이용한 플로우 개선 

## 개선 후 Architecture
<img width="1201" alt="image" src="https://user-images.githubusercontent.com/61778930/183723902-cdd2552f-e8bb-42a2-97bf-0de1526f0a8b.png">

## State Machine 구성
![stepfunctions_graph (14)](https://user-images.githubusercontent.com/61778930/183724171-fbbe33db-fb8d-409d-b3e4-c270153f3afc.png)

### 주요 개선 사항
1. Lambda 분리 후 병렬화: SSB 항목을 체크하는 로직을 4개의 Lambda로 분리한 후, Step Functions를 이용해 Lambda를 병렬 처리 해주었습니다. 이때, 메모리 이슈 등 병렬화와 관련된 상태 관리를 모두 Step Functions가 진행해 줍니다. 
2. Step Functions를 이용한 오류 처리: 기존에 코드를 반복적으로 `try ~ except` 구문을 사용하며 에러 처리를 진행했지만, Step Functions를 이용해 간편하게 에러 핸들링을 진행하게 되면서 불필요한 상태 관리 코드를 삭제할 수 있게 되었습니다. 

## Proof of Concept
### 📌 실행 시간 관점
기존 18971ms가 걸리던 워크로드가 Step Functions으로 개선 후 12279ms로 감소하였습니다. (약 36% 효율성 증가)

<img width="792" alt="image" src="https://user-images.githubusercontent.com/61778930/183727708-c0edb0d1-4401-4535-80ba-8aa08da2fce3.png">


### 📌 비용 관점
latency 이슈를 해결하기 위해 Lambda의 메모리 할당량을 늘렸을 때, 비슷한 수준의 효율성을 내는 조건에서 Step Functions를 이용한 애플리케이션이 가장 비용 절감 효과가 있었습니다. 

<img width="733" alt="image" src="https://user-images.githubusercontent.com/61778930/183727981-e1c060c6-f949-4eda-8265-dc8e4b426bdf.png">

- - -

# How to deploy this Application

1. 터미널을 열고 아래 명령어를 입력하여, 해당 Repository를 Clone 하고 디렉토리로 들어갑니다:
    ``` 
    git clone https://github.com/ottl-seo/SSB-stepfunctions
    cd SSB-stepfunctions
    ```
2. 터미널에 아래 명령어를 입력합니다. AWS SAM을 이용하여 template.yaml파일에 정의된 리소스를 배포하는 과정입니다:
    ```
    sam deploy --guided
    ```
3. Prompt에 아래와 같은 입력값이 요구됩니다. 본인의 환경에 맞춰 입력해주세요:
    * `stack name`: ssb-app (또는 본인이 원하는 스택 이름을 입력 가능합니다)
    * `desired AWS Region`: ap-northeast-1 (또는 원하는 AWS 리전을 입력 가능합니다)
    * Allow SAM CLI to create IAM roles with the required permissions.

4. 이후 스택이 배포되며, 입력한 이메일로 SNS Topic 구독을 요청하는 이메일이 발송됩니다. 메일의 `Confirm subscrption`을 클릭하여 먼저 알림을 구독해주세요.
    <img width="1415" alt="image" src="https://user-images.githubusercontent.com/61778930/184087809-e98adb74-a45d-4c8b-af5e-f478e0c8c8ef.png">


4. [AWS Step Functions 콘솔](https://ap-northeast-1.console.aws.amazon.com/states/home?region=ap-northeast-1#/statemachines)로 이동하여, 생성된 상태머신을 `실행 시작` 버튼을 눌러 실행합니다. 
    ![image](https://user-images.githubusercontent.com/61778930/184089355-bf36b7b9-7a1e-49a2-8c57-01ab7045a913.png)

5. 이후 상태머신이 아래와 같이 실행되며, SNS 구독을 한 이메일로 리포트를 다운로드할 수 있는 URL이 발송됩니다. 
    <img width="1127" alt="image" src="https://user-images.githubusercontent.com/61778930/184089516-64d2e104-ad21-46c6-b559-1ce382a1627e.png">

6. URL에 접근하여 아래와 같은 리포트를 확인하실 수 있습니다. 
    <img width="783" alt="image" src="https://user-images.githubusercontent.com/61778930/184091694-ee013745-057f-4eb6-9c87-193cd20a7cb8.png">


- - -

## Workshop

애플리케이션의 내용과 사용 방법에 대한 자세한 안내는 [Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR)을 참고해주세요. 

- - - 
#### Contributor
- Yoonseo Kim: Refactoring SSB with Step Functions and Conducting PoC
- Kihoon Kwon: Developing SSB Application
