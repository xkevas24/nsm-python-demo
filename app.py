from flask import Flask, request
import requests
import socket
import netifaces
app = Flask(__name__)


def returner(code, msg, data):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }


def get_local_ip():
    ips = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo':  # 跳过回环接口
            continue
        iface = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if iface:
            for ip in iface:
                ips.append(ip['addr'])
    return ips


@app.route('/', methods=["GET"])
def welcome():
    return 'Welcome to use Netease Qingzhou Cloud Native Service!'


@app.route('/ping', methods=["GET"])
def ping():
    # 获取本地ip
    return returner(200, "echo from", get_local_ip())


@app.route('/access_http', methods=["GET", "POST"])
def access():
    # 输入需要被调用的服务名
    if "service_name" in request.args:
        service_name = request.args.get("service_name")
    else:
        return returner(403, "failed", "[service_name] is required")

    # 输入被调用的服务的端口号，默认为80
    if "service_port" in request.args:
        service_port = request.args.get("service_port")
    else:
        service_port = 80

    # 输入被调用的服务的方式，默认为GET，可选GET和POST
    if "method" in request.args:
        method = request.args.get("method")
        if method != "GET" and method != "POST":
            return returner(403, "failed", "[method] should be GET or POST")
    else:
        method = "GET"

    # 输入被调用服务的api
    if "api" in request.args:
        api = request.args.get("api")
    else:
        return returner(403, "failed", "[api] like /health is required")

    url = "http://{}:{}{}".format(service_name, service_port, api)
    print(url)
    # POST方式需要携带payload，通过请求本接口时携带
    if method == "POST":
        POST_JSON = request.json
        try:
            response = requests.post(url, data=POST_JSON)
        except Exception as e:
            return returner(501, "Exception", str(e))
    else:
        try:
            response = requests.get(url)
        except Exception as e:
            return returner(501, "Exception", str(e))
    return returner(200, "ok", response.text)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)


