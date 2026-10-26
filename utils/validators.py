from datetime import datetime

from exceptions import param_error

DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)


def parse_int(value, default, name, min_value=None, max_value=None):
    """解析整型参数，非法或越界抛参数异常"""
    if value is None or value == "":
        return default
    try:
        result = int(value)
    except (TypeError, ValueError):
        raise param_error("参数 %s 必须为整数" % name)
    if min_value is not None and result < min_value:
        raise param_error("参数 %s 不能小于 %s" % (name, min_value))
    if max_value is not None and result > max_value:
        raise param_error("参数 %s 不能大于 %s" % (name, max_value))
    return result


def parse_datetime(value, name):
    """解析时间参数，非法格式抛参数异常"""
    if value is None or value == "":
        return None
    for fmt in DATETIME_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise param_error("参数 %s 时间格式错误，支持格式：YYYY-MM-DD HH:MM:SS" % name)
