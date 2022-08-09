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
비슷한 수준의 효율성을 내는 조건에서, Step Functions를 이용한 애플리케이션이 가장 비용 절감 효과가 있었습니다. 

<img width="733" alt="image" src="https://user-images.githubusercontent.com/61778930/183727981-e1c060c6-f949-4eda-8265-dc8e4b426bdf.png">

- - -

## Workshop

애플리케이션의 내용과 사용 방법에 대한 자세한 안내는 [Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/43af4c8d-a61e-4b61-ad43-36f1a64804df/ko-KR)을 참고해주세요. 
