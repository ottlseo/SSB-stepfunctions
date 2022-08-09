import datetime
header = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    </meta>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </meta>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    </link>
    <title>Report</title>
</head>

<body><svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z">
            </path>
        </symbol>
        <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z">
            </path>
        </symbol>
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z">
            </path>
        </symbol>
    </svg>"""

footer = """
            </div>
            <div class="col"></div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2"
        crossorigin="anonymous"></script>
</body>

</html>"""

def generate_summary(account, date, danger, warning, success, error):

    return f"""    
    <div class="container">
        <div class="row">
            <div class="col"></div>
            <div class="col-9">
                <h1 class="text-center">SSB Self-Test Report</h2>
                <h3>Summary</h3>
                <div class="row">
                    {generate_table({
                        "cols": [],
                        "rows": [
                            ["Account", account],
                            ["Generated", date]
                        ]
                    })}
                </div>
                <div class="row">
                    <div class="card">
                        <div class="card-body">
                            <div class="alert alert-danger d-flex align-items-center" role="alert"><svg aria-label="Danger:"
                                    class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                    <use xlink:href="#exclamation-triangle-fill"></use>
                                </svg>
                                [Danger] 아래 내용을 빠르게 조치하지 않을 경우, 계정 침해 등의 보안 사고가 발생할 수 있습니다.
                            </div>
                            <ul class="list-group">
                                {generate_li(danger, 'danger')}
                            </ul>
                        </div>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="card">
                        <div class="card-body">
                            <div class="alert alert-warning d-flex align-items-center" role="alert"><svg aria-label="Warning:"
                                    class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                    <use xlink:href="#exclamation-triangle-fill"></use>
                                </svg>
                                [Warning] 아래 내용을 검토하여 계정의 보안을 강화해주세요.
                            </div>
                            <ul class="list-group">
                                {generate_li(warning, 'warning')}
                            </ul>
                        </div>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="card">
                        <div class="card-body">
                            <div class="alert alert-success d-flex align-items-center" role="alert"><svg aria-label="Success:"
                                    class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                    <use xlink:href="#check-circle-fill"></use>
                                </svg>
                                [Success] 계정 보안 사항이 준수되고 있지만, 정확한 내용을 다시 한번 확인해주세요.
                            </div>
                            <ul class="list-group">
                                {generate_li(success, 'success')}
                            </ul>
                        </div>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="card">
                        <div class="card-body">
                            <div class="alert alert-danger d-flex align-items-center" role="alert"><svg aria-label="Danger:"
                                    class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                    <use xlink:href="#exclamation-triangle-fill"></use>
                                </svg>
                                [Error] 아래 항목을 진단 중 권한 등의 문제로 오류가 발생하였습니다. 자세한 사항은 Details 항목을 확인해주세요.
                            </div>
                            <ul class="list-group">
                                {generate_li(error, 'error')}
                            </ul>
                        </div>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                            class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                            <use xlink:href="#info-fill"></use>
                        </svg>
                        계정 보안을 위한 추가적인 사항은 &nbsp<a href="https://www.awsstartup.io/security/network-security/aws-tip" target="_blank">[계정 안전하게 지키기 Tip]</a>&nbsp을 참고해주세요.
                    </div>
                </div>
            </div>
            <div class="col"></div>
        </div>
        <div class="row">
            <div class="col"></div>
            <div class="col-9">
            <h3>Details</h3>
            <div class="row">
                <div class="card">
                    <div class="card-body">
                        <div class="accordion" id="accordionPanelsStayOpenExample">
            """

def generate_li(items, level):
    ret = ""
    for item in items:

        testNum = item[5:7]

        ret += f'''<li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                <a href="#panelsStayOpen-heading{testNum}" onclick="document.querySelector('#panelsStayOpen-heading{testNum} button').click()"> {item} </a>
            </div>
            <span class="badge text-bg-{"danger" if level == "error" else level} rounded-pill">{level.capitalize()}</span>
            </li>'''
            
    if len(items) == 0:
        ret += f'''<li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                해당 사항이 없습니다.
            </div>
            <span class="badge text-bg-{"danger" if level == "error" else level} rounded-pill">{level.capitalize()}</span>
            </li>'''
        
    return ret

def generate_alert(title, level, msg):
    icons = {
        "Info": ["alert-primary", "#info-fill"],
        "Success": ["alert-success", "#check-circle-fill"],
        "Warning": ["alert-warning", "#exclamation-triangle-fill"],
        "Danger": ["alert-danger", "#exclamation-triangle-fill"],
        "Error": ["alert-danger", "#info-fill"],
    }

    code = ""
    if title != "":
        code = title.split()[0]

    return f"""
    <div class="alert {icons[level][0]} d-flex align-items-center" role="alert">
        <svg aria-label="{level}:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
            <use xlink:href="{icons[level][1]}"></use>
        </svg>
        <span>{code} {msg}</span>
    </div>
    """
def generate_table(table):

    cols = table["cols"]
    rows = table["rows"]
    
    ret = """<table class="table">"""
    for col in cols:
        ret += f"""<th scope="col">{col}</th>"""

    for row in rows:
        ret += """<tr>"""
        for e in row:
            ret += f"""<td>{e}</td>"""
        ret += """</tr>"""

    ret +="""</table>"""

    return ret

def generate_content(result):

    title = result["title"]
    alerts = result["alerts"]
    tables = result["tables"]

    success = 0
    warning = 0
    danger = 0

    for alert in alerts:
        if alert["level"] == "Success": success += 1
        elif alert["level"] == "Warning": warning += 1
        elif alert["level"] == "Danger": danger += 1

    content = f"""
        <div class="accordion-item">
          <h2 class="accordion-header" id="panelsStayOpen-heading{title[:2]}">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{title[:2]}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{title[:2]}">
                <b>{title} </b> - ({danger} Danger / {warning} Warning / {success} Success)
            </button>
          </h2>
          <div id="panelsStayOpen-collapse{title[:2]}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{title[:2]}">
            <div class="accordion-body">
    """

    for alert in alerts:
        content += generate_alert(alert.get("title", ""), alert["level"], "&nbsp".join(map(generate_msg, alert["msg"])))

    # for table in tables:
    for table in tables:
        content += generate_table(table)

    content += """
            </div>
        </div>
    </div>
    """
    
    return content

def generate_msg(msg):
    if msg["link"] == "":
        return msg["text"]
    return f"""<a href="{msg["link"]}" target="_blank">
                {msg["text"]}</a>"""


def generate_report(account, results):

    date = datetime.datetime.now().isoformat()
    report = ""
    report += header

    danger = []
    warning = []
    success = []
    error = []

    for result in results:
        for alert in result["alerts"]:
            if alert["level"] == "Danger": danger.append(alert["title"])
            elif alert["level"] == "Warning": warning.append(alert["title"])
            elif alert["level"] == "Success": success.append(alert["title"])
            elif alert["level"] == "Error": error.append(alert["title"])

    report += (generate_summary(account, date, danger, warning, success, error))

    contents = ""
    for result in results:
        contents += generate_content(result)
    contents += "</div></div></div></div>"
    
    report += contents
    report += footer
    
    return report