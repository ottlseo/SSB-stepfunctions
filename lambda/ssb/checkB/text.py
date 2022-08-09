
test5_1 = {
    # [Danger] CloudTrail이 켜저있는지

    "title": "[Test05-1] CloudTrail이 켜져있는지 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "CloudTrail 모두 켜저있습니다.", "link": ""}
        ]
    },

    "NO_TRAIL": {
        "level": "Danger",
        "msg": [
                {"text": "Trail이 존재하지 않습니다.", "link":""}, 
                {"text":"CloudTrail을 켜주세요.", "link": "https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html"}
            ]
    },

    "ALL_OFF": {
        "level": "Danger",
        "msg": [
            {"text": "모든 CloudTrail이 꺼져있습니다. 보안을 위해 CloudTrail의 로깅을 켜주세요.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "일부 CloudTrail이 꺼져있습니다. 보안을 위해 CloudTrail의 로깅을 켜주세요.", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test5_2 = {
    # [Danger] CloudTrail이 Multi-region으로 설정되어 있는지

    "title": "[Test05-2] CloudTrail이 Multi-region으로 설정되어 있는지 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "CloudTrail 모두 Multi-region 설정되어 있습니다.", "link": ""}
        ]
    },

    "NO_TRAIL": {
        "level": "Danger",
        "msg": [
                {"text": "Trail이 존재하지 않습니다.", "link":""}, 
                {"text":"CloudTrail을 켜주세요.", "link": "https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html"}
            ]
    },

    "NO_MULTI": {
        "level": "Warning",
        "msg": [
            {"text": "모든 CloudTrail이 Multi-region으로 설정되어 있지 않습니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "일부 CloudTrail이 Multi-region으로 설정되어 있지 않습니다.", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}


test7 = {
    # [Warning] 비용 알람 및 루트 계정 엑세스 알람

    "title": "[Test07] 비용 알람 및 루트 계정 엑세스 알람 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "알람이 켜져있습니다. 비용 및 루트 계정 알람인지 확인해 주세요.", "link": ""}
        ]
    },

    "NO_ALARM": {
        "level": "Warning",
        "msg": [
                {"text": "알람이 설정되어있지 않습니다. 보안을 위해 알람을 설정해주세요.", "link":""}, 
            ]
    },
    
    "Info": {
        "level": "Info",
        "msg": [
                {"text": "워크샵", "link": "https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms"},
                {"text": "을 통하여 비용 및 루트 계정 알람을 설정할 수 있습니다.", "link": ""}
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}
