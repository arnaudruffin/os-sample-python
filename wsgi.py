from flask import Flask
from requests import get
import os

application = Flask(__name__)

TARGET="https://plazza.orange.com/api/"

@application.route("/")
def hello():
    return "Hello You!"

@application.route("/api/<path:path>", methods=["GET"])
def proxy(path):
    redirection = "%s%s" % (TARGET,path)
    println(redirection)
    user = os.environ['USER']
    password = os.envion["PASS"]
    return get(redirection,auth=(user,password)).content

if __name__ == "__main__":
    application.run()
