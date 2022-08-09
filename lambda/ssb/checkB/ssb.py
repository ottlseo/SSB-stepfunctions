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


def check05(session):

    s = time.time()

    title = "05 Turn CloudTrail On"
    cloudtrail = session.client('cloudtrail')

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["Trail", "multi region", "logging"],
                "rows": []
            }
        ]
    }

    code = "Success"
    code_multi_region = "Success"
    logging = 0
    multi_region = 0
    errorMsg = ""

    try:

        trails = cloudtrail.describe_trails()["trailList"]

        if len(trails) == 0:
            # utils.print_fail("No trails exists")
            code = "NO_TRAIL"
            code_multi_region = "NO_TRAIL"

        for trail in trails:
            # print(trail["TrailARN"])
            if(trail["IsMultiRegionTrail"]):
                # utils.print_pass("Multi region trail: True")
                multi_region += 1
            else:
                # utils.print_fail("Multi region trail: False")
                code_multi_region = "Warning"

            status = cloudtrail.get_trail_status(Name=trail["TrailARN"])
            if(status["IsLogging"]):
                # utils.print_pass("logging: True")
                logging += 1

            else:
                # utils.print_fail("logging: False")
                # append_alert(ret, "Danger", [[f"{trail['TrailARN']}가 logging되고 있지 않습니다.", ""]])
                code = "Warning"

            append_table(ret, 0, [trail["TrailARN"], trail["IsMultiRegionTrail"], status["IsLogging"]])
        
        if code != "NO_TRAIL" and logging == 0:
            code = "ALL_OFF"

        if code != "NO_TRAIL" and multi_region == 0:
            code_multi_region = "NO_MULTI"

    except botocore.exceptions.ClientError as error:
        errorMsg = error.response["Error"]["Message"]
        code = "Error"



    ret["alerts"].append({
        "level": text.test5_1[code]["level"],
        "msg": text.test5_1[code]["msg"] + [{"text":errorMsg, "link":""}],
        "title": text.test5_1["title"]
    })

    if code != "Error":
        ret["alerts"].append({
            "level": text.test5_2[code_multi_region]["level"],
            "msg": text.test5_2[code_multi_region]["msg"] + [{"text":errorMsg, "link":""}],
            "title": text.test5_2["title"]
        })

    print(title, time.time() - s)

    return ret

def check07(session):

    s = time.time()

    title = "07 Configure Alarms"
    alarms_tot = []
    
    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["리전", "이름"],
                "rows": []
            }
        ]
    }

    regions = sorted(list(map(lambda x: x["RegionName"], session.client("ec2").describe_regions()["Regions"])))
    _executor = ThreadPoolExecutor(20)

    async def run(region):
        loop = asyncio.get_running_loop()
        cloudwatch = session.client("cloudwatch", region_name=region)
        response = await loop.run_in_executor(_executor, cloudwatch.describe_alarms)
        return response

    async def execute():
        task_list = [asyncio.ensure_future(run(region)) for region in regions]
        done, _ = await asyncio.wait(task_list)

        results = [d.result() for d in done]
        return results

    code = "Success"
    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(execute())
        loop.close()

        for result in results:
            for alarm in result["MetricAlarms"]:
                arn = alarm["AlarmArn"].split(":")
                region = arn[3]
                name = arn[6]
                alarms_tot.append((region, name))
            

        for alarm in alarms_tot:
            append_table(ret, 0, [alarm[0], alarm[1]])


        if len(alarms_tot) == 0:
            code = "NO_ALARM"
        else:
            code = "Success"

    except botocore.exceptions.ClientError as error:
        code = "Error"
        errorMsg = error.response["Error"]["Message"]

    ret["alerts"].append({
        "level": text.test7[code]["level"],
        "msg": text.test7[code]["msg"],
        "title": text.test7["title"]
    })
    
    ret["alerts"].append({
        "level": text.test7["Info"]["level"],
        "msg": text.test7["Info"]["msg"],
        "title": text.test7["title"]
    })


    print(title, time.time() - s)

    return ret

async def generate_async_check(check, session, _executor):

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(_executor, check, session)
    return response
    


async def async_checks(session, _executor, tests):

    checks = [check05, check07]

    task_list = [asyncio.ensure_future(generate_async_check(checks[i-1], session, _executor)) for i in tests]
    

    done, _ = await asyncio.wait(task_list)
    results = [d.result() for d in done]

    return results

def checks(session, tests=[1,2]):

    _executor = ThreadPoolExecutor(5)

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

    print(check07(session))
