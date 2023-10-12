import json
import sys
from flask import Flask, request
from flask_cors import CORS
import requests
import socket
import netifaces
app = Flask(__name__)


def after_request(resp):
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


app.after_request(after_request)
CORS(app)


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
    return returner(200, "response message", {
        "ips": get_local_ip(),
        "headers": str(request.headers)
    })


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


@app.route('/get_version', methods=["GET"])
def get_version():
    # 获取本地ip
    color_mark = request.headers.get('X-Nsf-Mark')
    return returner(200, "ok", {
        "version": "V1.0.0",
        "notes": "提供产品的详细介绍信息，为product-info提供年化利率的数据（非核心）",
        "ips": get_local_ip(),
        "headers": str(request.headers),
        "color_mark": color_mark
    })


@app.route('/get_product_detail', methods=["GET"])
def get_product_detail():
    # 获取本地ip

    return returner(200, "ok", [
        {
            "title": "财富管家-初级版",
            "detail": "财富管家-中级版主要投向中高等级<span style='color: #1976D2'>中短期债券</span>，远离股市波动。所投债券资产久期较短且信用等级较高，相对能更好地控制风险，力争匹配投资者的<span style='color: #1976D2'>短期闲钱理财需求</span>。"     # "<span style='color: #FE0000'>这是一个bug，本来这里要显示文字的！</span>"
        },
        {
            "title": "财富管家-中级版",
            "detail": "财富管家-中级版主要投向中高等级<span style='color: #1976D2'>中短期债券</span>，远离股市波动。所投债券资产久期较短且信用等级较高，相对能更好地控制风险，力争匹配投资者的<span style='color: #1976D2'>短期闲钱理财需求</span>。"
        },
        {
            "title": "财富管家-高级版",
            "detail": "财富管家-高级版主要投向中高等级<span style='color: #1976D2'>中短期债券</span>，远离股市波动。所投债券资产久期较短且信用等级较高，相对能更好地控制风险，力争匹配投资者的<span style='color: #1976D2'>短期闲钱理财需求</span>。"
        },
        {
            "title": "财富管家-终身版",
            "detail": "财富管家-终身版主要投向中高等级<span style='color: #1976D2'>中短期债券</span>，远离股市波动。所投债券资产久期较短且信用等级较高，相对能更好地控制风险，力争匹配投资者的<span style='color: #1976D2'>短期闲钱理财需求</span>。"
        },
    ])


@app.route('/get_annual', methods=["GET"])
def get_annual():
    product_name = request.args.get("product_name")
    annual = "0.00%"
    if product_name == "财富管家-初级版":
        annual = "3.33%"
    if product_name == "财富管家-中级版":
        annual = "3.60%"
    if product_name == "财富管家-高级版":
        annual = "4.49%"
    if product_name == "财富管家-终身版":
        annual = "5.06%"
    return annual


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    app.run(host='0.0.0.0', port=port)


