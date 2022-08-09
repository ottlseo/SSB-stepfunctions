import report
import ssb
import boto3

session = boto3.Session()

try:
    results = ssb.checks(session)
    results.sort(key=lambda x: x["title"])

    try:
        sts = session.client("sts")
        account = sts.get_caller_identity()["Account"]
        html = report.generate_report(account, results)

        with open('./report.html', 'w') as f:
            f.write(html)

    except:
        print("리포트 생성 중 오류가 발생하였습니다.")

except Exception as e:
    print('진단 중 오류가 발생하였습니다.')