import json
import argparse
import sys
from urllib.parse import urlencode
from flask import Flask, request, abort
from flask_cors import CORS
import requests
import socket
import netifaces
import random
import time

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
    return 'Welcome to use Netease Qingzhou Cloud Native Service! - {}'.format(version)
    # return 'Break', 299


@app.route('/version', methods=["GET"])
def return_version():
    return returner(200, "ok", version)


@app.route('/ping', methods=["GET"])
def ping():
    # 获取本地ip
    return returner(200, "response message", {
        "version": version,
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
        api = "/"

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
    return returner(response.status_code, "ok", response.text)


@app.route('/detail/get_version', methods=["GET"])
def get_version():
    # 获取本地ip
    # color_mark = request.headers.get('X-Nsf-Mark')
    return returner(200, "ok", {
        "version": version,
        "notes": "提供产品的详细介绍信息，为product-info提供年化利率的数据（非核心）",
        "ips": get_local_ip(),
        "headers": str(request.headers),
        "color_mark": color_instance
    })


@app.route('/info/get_version', methods=["GET"])
def get_version_info():
    # 获取本地ip
    # color_mark = request.headers.get('X-Nsf-Mark')
    return returner(200, "ok", {
        "version": version,
        "notes": "提供产品的名称和价格",
        "ips": get_local_ip(),
        "headers": str(request.headers),
        "color_mark": color_instance
    })


@app.route('/detail/get_product_detail', methods=["GET"])
def get_product_detail():
    # 获取本地ip

    return returner(200, "ok", [
        {
            "title": "财富管家-初级版",
            "detail": "财富管家-低级版主要投向低等级<span style='color: #1976D2'>短期债券</span>，远离股市波动。所投债券资产久期较短且信用等级较高，相对能更好地控制风险，力争匹配投资者的<span style='color: #1976D2'>短期闲钱理财需求</span>。"
            # "<span style='color: #FE0000'>这是一个bug，本来这里要显示文字的！</span>"
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


@app.route('/detail/get_annual', methods=["GET"])
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


@app.route('/info/get_product', methods=["GET"])
def info_get_product():
    return returner(200, "ok", [
        {
            "title": "财富管家-初级版",
            "img": "lv1.webp",
            "basic": "3.33%",
            "notice": "30天｜10元起购｜中低风险｜债券基金"
        },
        {
            "title": "财富管家-中级版",
            "img": "lv2.webp",
            "basic": "3.60%",
            "notice": "30天｜20元起购｜中低风险｜债券基金"
        }, {
            "title": "财富管家-高级版",
            "img": "lv3.webp",
            "basic": "4.49",
            "notice": "30天｜30元起购｜中低风险｜债券基金"
        }, {
            "title": "财富管家-终身版",
            "img": "lv4.webp",
            "basic": "5.06%",
            "notice": "120天｜100元起购｜中低风险｜债券基金"
        }
    ])


@app.route('/unstable', methods=["GET"])
def unstable():
    # 这个接口需要有一定的概率返回500

    if "code" in request.args:
        code = int(request.args.get("code"))
    else:
        code = 500

    if "chance" in request.args:
        chance = float(request.args.get("chance"))
    else:
        chance = 0.5

    if chance == 1:
        return 'Error!', code
    if random.random() < chance:
        # abort(500)
        return 'Error!', code
    else:
        return 'Work!'


def simulate_cpu_usage():
    while True:
        pass


@app.route('/cpu_max', methods=["GET"])
def cpu_max():
    simulate_cpu_usage()
    return 'Reach!'


@app.route('/delay_return', methods=["GET"])
def delay_return():
    if "seconds" in request.args:
        seconds = int(request.args.get("seconds"))
    else:
        seconds = 2
    time.sleep(seconds)  # 2秒延迟
    return "Delayed response after {} seconds".format(seconds)


def api(entry, params, color_mark):
    try:
        print("http://{}?{}".format(entry, params))
        print("color_mark:".format(color_mark))
        if color_mark is not None:
            headers = {"X-Nsf-Mark": color_mark}
            response = requests.get("http://{}?{}".format(entry, params), headers=headers)
        else:
            response = requests.get("http://{}?{}".format(entry, params))
    except Exception as e:
        return returner(501, "Exception", str(e))
    return response.content


@app.route('/api', methods=["GET"])
def api_redirect():
    if "entry" in request.args:
        entry = request.args.get("entry")
    else:
        return returner(403, "failed", "[entry] is required")

    if "color_mark" in request.args:
        color_mark = request.args.get("color_mark")
    else:
        color_mark = None
    # color_mark = request.headers.get('X-Nsf-Mark')
    print(request.headers)
    # print(color_mark)
    return api(entry, urlencode(request.args), color_mark)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', '--port', help='设置demo启动端口，默认为8081')
    parser.add_argument('-version', '--version', help='设置DEMO显示的版本名称，默认为V1.0.0')
    parser.add_argument('-color', '--color', help='设置实例的染色标识，默认为五色')
    args = parser.parse_args()
    if args.port is None:
        port = 8081
    else:
        port = int(args.port)
    print("DEMO PORT: {}".format(port))

    if args.version is None:
        version = "V1.0.0"
    else:
        version = args.version
    print("DEMO VERSION: {}".format(version))

    if args.color is None:
        color_instance = None
    else:
        color_instance = args.color
    print("DEMO COLOR: {}".format(color_instance))

    app.run(host='0.0.0.0', port=port)
