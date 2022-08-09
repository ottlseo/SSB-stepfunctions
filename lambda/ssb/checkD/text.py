
test9 = {
    # [Warning] Trusted Advisor 설정 여부

    "title": "[Test09] Trusted Advisor 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "Trusted Advisor가 작동 중 입니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
                {"text": "Trusted Advisor가 꺼져있습니다.", "link":""}, 
            ]
    },

    "Subscribe": {
        "level": "Warning",
        "msg": [
                {"text": " Business Support 이상의 Support Plan 을 이용하시면 Trusted Advisor 에서 더 다양한 지표들에 대해 점검하고 조치 가이드를 받으실 수 있습니다.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test10 = {
    # [Warning] GuardDuty 설정 여부

    "title": "[Test10] GuardDuty 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "GuardDuty가 작동 중 입니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
                {"text": "GuardDuty가 꺼져있습니다.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}