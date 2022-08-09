test1 = {
    # [Warning] 대체 연락처 정보가 모두 입력되어있는지 확인

    "title": "[Test01] 대체 연락처 정보 입력 여부",

    "Success": {
        "level": "Success",
        "msg": [{"text": "대체 연락처 정보가 모두 입력되어 있습니다. 정확한 정보인지 확인해주세요.", "link": ""}]
    },

    "Warning": {
        "level": "Warning",
        "msg": [{"text": "일부 연락처 정보가 누락되어 있습니다. 연락처 정보를 등록해주세요.", "link": ""}]
    },

    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    },

    "Info": {
        "level": "Info",
        "msg": [
            {"text":"루트 계정을 포함한", "link":""},
            {"text": "연락처 정보 확인", "link": "https://us-east-1.console.aws.amazon.com/billing/home?region=us-east-1#/account"}
        ]
    }
}

test2_1 = {
    # [Danger] 1일 이내에 루트 계정 엑세스가 존재하는지 확인

    "title": "[Test02-1] 루트 계정 엑세스 여부",

    "Success": {
        "level": "Success",
        "msg": [{"text": "1일 이내에 루트 계정으로 엑세스한 기록이 없습니다.", "link": ""}]
    },

    "Danger": {
        "level": "Danger",
        "msg": [{"text": "1일 이내에 루트 계정으로 엑세스한 기록이 존재합니다. 루트 계정으로 직접 AWS의 서비스를 이용하지 마세요.", "link": ""}]
    },

    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }
}

test2_2 = {
    # [Danger] 루트 계정에 MFA가 설정되어 있는지 확인
    "title": "[Test02-2] 루트 계정 MFA 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [{"text": "루트 계정에 MFA가 설정되어 있습니다.", "link": ""}]
    },

    "Danger": {
        "level": "Danger",
        "msg": [
            {"text": "루트 계정에 MFA가 설정되어 있지 않습니다. 링크를 통해 설정해주세요.", "link": ""},
            {"text": "(루트 계정 MFA 설정)", "link": "https://us-east-1.console.aws.amazon.com/billing/home?region=us-east-1#/account"}
        ]
    },

    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test2_3 = {
    # [Danger] 루트 계정에 Access Key가 생성되어 있는지 확인

    "title": "[Test02-3] 루트 계정 Access Key 생성 여부",

    "Success": {
        "level": "Success",
        "msg": [{"text": "루트 계정에 Access Key가 생성되어 있지 않습니다.", "link": ""}]
    },

    "Danger": {
        "level": "Danger",
        "msg": [
        {"text": "루트 계정에 Access Key가 생성되어 있습니다. 루트 계정의 Access Key를 삭제해주세요.", "link": ""},
        {"text": "(Access Key 삭제)", "link": "https://us-east-1.console.aws.amazon.com/billing/home?region=us-east-1#/account"}
        ]
    },

    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }
}

test3_1 = {
    # [Warning] IAM User에 MFA 설정이 되어있는지 확인

    "title": "[Test03-1] IAM User MFA 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "모든 IAM User에 MFA 설정이 되어있습니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "일부 IAM User에 MFA 설정이 되어있지 않습니다.", "link": ""}
        ]
    },

    "NO_USER": {
        "level": "Danger",
        "msg": [
            {"text": "IAM User가 존재하지 않습니다. 루트 계정으로 직접 AWS의 서비스를 이용하지 마세요", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test3_2 = {
    # [Warning] Password 정책이 있는지 확인

    "title": "[Test03-2] 패스워드 정책 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "패스워드 정책이 설정되어 있습니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "패스워드 정책이 설정되어있지 않습니다.", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test4 = {
    # [Warning] IAM User에 Policy를 직접 할당했는지

    "title": "[Test04] IAM User에 Policy 할당 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "IAM User에 Policy가 직접 할당되어 있지 않습니다.", "link": ""}
        ]
    },

    "NO_USER": {
        "level": "Danger",
        "msg": [
            {"text": "IAM User가 존재하지 않습니다. 루트 계정으로 직접 AWS의 서비스를 이용하지 마세요", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "특정 IAM User에 Policy가 직접 할당되어 있습니다. IAM Group을 통해 할당해주세요.", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

