from flask import Flask, abort, Response, request
import requests 
import os

application = Flask(__name__)

TARGET="https://plazza.orange.com/api/"

@application.route("/")
def hello():
    return "Hello You!"

@application.route("/api/<path:path>", methods=["OPTIONS"])
def hande_preflight(path):
    return "You rule, preflight!"

@application.route("/api/<path:path>", methods=["GET"])
def proxy(path):
    url = "%s%s?%s" % (TARGET,path,request.query_string.decode("utf-8"))
    print(url)
    print(request.query_string)
    user = os.environ['USER']
    password = os.environ["PASS"]
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "cecfaf76-0b4b-4e37-8fb6-d1e4b01a0288",
    'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    req = requests.get(url, auth=(user, password), headers=headers)
    if((req.status_code == requests.codes.ok) or (req.status_code == 201)):
        return req.content
    else:
        print("Error: ")
        print(req.status_code)
        print(req.text)
        print(req.headers)
        print(req)
        #abort(req.status_code)
        #abort(Response(req.text))
        return req
        #return "Error"

if __name__ == "__main__":
    application.run()
