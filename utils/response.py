from flask import jsonify


class Code:
    """统一返回码"""
    SUCCESS = 0        # 成功
    PARAM_ERROR = 40001   # 参数校验失败
    NOT_FOUND = 40401     # 资源不存在
    SERVER_ERROR = 50000  # 服务器内部错误


def success(data=None, msg="success"):
    """成功响应"""
    return jsonify({"code": Code.SUCCESS, "msg": msg, "data": data})


def fail(code, msg, data=None, http_status=200):
    """失败响应，http_status 为对应的 HTTP 状态码"""
    resp = jsonify({"code": code, "msg": msg, "data": data})
    resp.status_code = http_status
    return resp
