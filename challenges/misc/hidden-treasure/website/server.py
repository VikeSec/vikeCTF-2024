from bottle import get, post, response, request, run

session_cookie = "6090a4914358dc1fce139aa4e11df13009c2eda2b75d35d537706d7313237389"

with open("login.html", "r") as f:
    failed_page = f.read()

normal_page = failed_page.replace("open", "")

with open("flag.html", "r") as f:
    flag_page = f.read()


@get("/")
def normal():
    if request.get_cookie("session") == session_cookie:
        return flag_page
    return normal_page


@post("/")
def failed():
    if request.get_cookie("session") == session_cookie:
        return flag_page
    response.status = 401
    return failed_page


run(host="0.0.0.0", port=8080, server="gunicorn")
