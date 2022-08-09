import botocore.exceptions
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

import sys, os
sys.path.append(os.path.dirname(__file__))
import text

def append_alert(ret, alert, title):
    ret["alerts"].append({
        "level": alert["level"],
        "msg": alert["msg"],
        "title": title
    })

def append_table(ret, num, row):
    ret["tables"][num]["rows"].append(row)

############## CHECK A ###############


def check01(session):
    s = time.time()
    title = "01 Accurate Information"
    account = session.client('account')

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["계정 타입", "이름", "이메일", "전화번호"],
                "rows": []
            }
        ]
    }

    level = "Success"
    errorMsg = ""
    
    for t in ["BILLING", "SECURITY", "OPERATIONS"]:
        try:
            contact = account.get_alternate_contact(AlternateContactType=t)["AlternateContact"]
            ret["tables"][0]["rows"].append([t, contact["Name"], contact["EmailAddress"], contact["PhoneNumber"]])

        except botocore.exceptions.ClientError as error :
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                level = "Warning"
                ret["tables"][0]["rows"].append([t, "", "정보 없음", ""])      
            else:
                errorMsg = error.response["Error"]["Message"]
                level = "Error"
    
    
    ret["alerts"].append({
        "level": text.test1["Info"]["level"],
        "msg": text.test1["Info"]["msg"]
    })

    ret["alerts"].append({
        "level": text.test1[level]["level"],
        "msg": text.test1[level]["msg"] + [{"text":errorMsg, "link": ""}],
        "title": text.test1["title"]
    })

    print(title, time.time() - s)

    return ret

def check02(session):

    s = time.time()

    title = "02 Protect Root User"
    iam = session.client('iam')

    def check_root_access(date):
        if date == "N/A" or date=="no_information":
            return timedelta(9999)

        return datetime.utcnow() - datetime.fromisoformat(date[:-6])

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["최근접속일", "MFA 설정", "Access Key1", "Access Key2"],
                "rows": []
            }
        ]
    }

    report_cols={
            "PASSWORD_LAST_USED": 4,
            "MFA": 7,
            "ACCESS_KEY1": 8,
            "ACCESS_KEY1_LAST_USED": 10,
            "ACCESS_KEY2": 13,
            "ACCESS_KEY2_LAST_USED": 15
        }

    
    try:
        response = iam.get_credential_report()
        report = response["Content"].decode('ascii').split()
        root_report = report[1].split(",")

        last_accessed = min(check_root_access(root_report[report_cols["PASSWORD_LAST_USED"]]), \
            check_root_access(root_report[report_cols["ACCESS_KEY1_LAST_USED"]]),\
                check_root_access(root_report[report_cols["ACCESS_KEY2_LAST_USED"]]))
        code = "Error"
        if last_accessed > timedelta(1):
            code = "Success"
        else:
            code = "Danger"

        ret["alerts"].append({
            "level": text.test2_1[code]["level"],
            "msg": text.test2_1[code]["msg"],
            "title": text.test2_1["title"]
        })

        if root_report[report_cols["MFA"]] == "true":
            code = "Success"
        else:
            code = "Danger"
    
        ret["alerts"].append({
            "level": text.test2_2[code]["level"],
            "msg": text.test2_2[code]["msg"],
            "title": text.test2_2["title"]
        })

        if root_report[report_cols["ACCESS_KEY1"]] == "false" and \
            root_report[report_cols["ACCESS_KEY2"]] == "false":
            code = "Success"
        else:
            code = "Danger"

        ret["tables"][0]["rows"].append([f"{last_accessed.days}일 전", root_report[report_cols["MFA"]], root_report[report_cols["ACCESS_KEY1"]], root_report[report_cols["ACCESS_KEY2"]]])

        ret["alerts"].append({
            "level": text.test2_3[code]["level"],
            "msg": text.test2_3[code]["msg"],
            "title": text.test2_3["title"]
        })

    except botocore.exceptions.ClientError as error :
        ret["alerts"].append({
            "title": text.test2_3["title"],
            "level": "Error",
            "msg": text.test2_3["Error"]["msg"] + [{"text": error.response["Error"]["Message"], "link":""}]
        })
  

    print(title, time.time() - s)

    return ret

def check03(session):

    s = time.time()

    title = "03 Create Users for Human Identities"

    iam = session.client('iam')

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["IAM User", "MFA 설정", "Access Key1", "Access Key2"],
                "rows": []
            }
        ]
    }

    report_cols={
        "PASSWORD_LAST_USED": 4,
        "MFA": 7,
        "ACCESS_KEY1": 8,
        "ACCESS_KEY1_LAST_USED": 10,
        "ACCESS_KEY2": 13,
        "ACCESS_KEY2_LAST_USED": 15
    }

    errorMsg = ""
    

    try:
        response = iam.get_credential_report()
        report = response["Content"].decode('ascii').split()
        users = list(map(lambda x: x.split(","), report[2:]))

        code = "Success"
        if(len(users) == 0):
            code = "NO_USER"

        for user in users:
            if user[report_cols["MFA"]] == "true":
                pass
            else:
                code = "Warning"

            ret["tables"][0]["rows"].append([user[0], user[report_cols["MFA"]], user[report_cols["ACCESS_KEY1"]], user[report_cols["ACCESS_KEY2"]]])

        ret["alerts"].append({
            "level": text.test3_1[code]["level"],
            "msg": text.test3_1[code]["msg"],
            "title": text.test3_1["title"]
        })

        # print("03-2 Checcking a password policy")
        code = "Error"
        try:
            policy = iam.get_account_password_policy()
            # utils.print_pass("Set strong password policy to protect account")
            code = "Success"
            

        except botocore.exceptions.ClientError as error :
            if error.response['Error']['Code'] == 'NoSuchEntity':
                # utils.print_fail("No password policy")
                code = "Warning"
            else:
                code = "Error"
                errorMsg = error.response["Error"]["Message"]

    except botocore.exceptions.ClientError as error:
        code = "Error"
        errorMsg = error.response["Error"]["Message"]

    ret["alerts"].append({
        "level": text.test3_2[code]["level"],
        "msg": text.test3_2[code]["msg"] + [{"text":errorMsg, "link": ""}],
        "title": text.test3_2["title"]
    })

    print(title, time.time() - s)

    return ret

def check04(session):

    s = time.time()

    title = "04 Use User Groups"
    iam = session.client('iam')


    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["IAM User", "Attached policies", "Inline policies"],
                "rows": []
            }
        ]
    }

    code = "Success"
    errorMsg = ""
    
    try:
        users = iam.list_users()["Users"]

        if(len(users) == 0):
            # utils.print_fail("No user exists to access console")
            code = "NO_USER"

        for user in users:
            attached = iam.list_attached_user_policies(UserName=user["UserName"])["AttachedPolicies"]
            inline = iam.list_user_policies(UserName=user["UserName"])["PolicyNames"]

            if len(attached) == 0:
                pass
            else:
                code = "Warning"

            if len(inline) == 0:
                pass
            else:
                code = "Warning"

            ret["tables"][0]["rows"].append([user["UserName"], len(attached), len(inline)])

    except botocore.exceptions.ClientError as error:
        code = "Error"
        errorMsg = error.response["Error"]["Message"]

    ret["alerts"].append({
        "level": text.test4[code]["level"],
        "msg": text.test4[code]["msg"] + [{"text":errorMsg, "link": ""}],
        "title": text.test4['title']
    })

    print(title, time.time() - s)

    return ret
    

async def generate_async_check(check, session, _executor):

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(_executor, check, session)
    return response
    


async def async_checks(session, _executor, tests):

    checks = [check01, check02, check03, check04]

    task_list = [asyncio.ensure_future(generate_async_check(checks[i-1], session, _executor)) for i in tests]
    

    done, _ = await asyncio.wait(task_list)
    results = [d.result() for d in done]

    return results

def checks(session, tests=[1,2,3,4]):

    _executor = ThreadPoolExecutor(8)

    try:
        iam = session.client('iam')
        iam.generate_credential_report()
    except:
        pass

    s = time.time()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_checks(session, _executor, tests))
    print(time.time() - s)

    return result
    
if __name__ == "__main__":
    import boto3
    session = boto3.Session()

    print(check04(session))
