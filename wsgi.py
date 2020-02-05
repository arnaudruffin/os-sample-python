import flask
import requests 
import os

application = flask.Flask(__name__)

TARGET="https://plazza.orange.com/api/"

@application.route("/")
def hello():
    return "Hello You!"

@application.route("/api/<path:path>", methods=["OPTIONS"])
def hande_preflight(path):
    return "You rule, preflight!"

@application.route("/old/<path:path>", methods=["GET"])
def old_school_proxy(path):
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
        req.headers['Access-Control-Allow-Origin'] = '*'
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


method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
}

@application.route("/api/<path:path>", methods=method_requests_mapping.keys())
def proxy(path):
    url = "%s%s?%s" % (TARGET,path,flask.request.query_string.decode("utf-8"))
    print(url)
    print(flask.request.query_string)
    user = os.environ['USER']
    password = os.environ["PASS"]
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "cecfaf76-0b4b-4e37-8fb6-d1e4b01a0288",
    'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }

    requests_function = method_requests_mapping[flask.request.method]
    #, params=flask.request.args
    rq = requests_function(url, auth=(user, password), headers=headers, stream=True)
    response = flask.Response(flask.stream_with_context(rq.iter_content()),
                              content_type=rq.headers['content-type'],
                              status=rq.status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    print(rq.url)
    print(response)
    return response

if __name__ == "__main__":
    application.run()
