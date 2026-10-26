from utils.response import Code


class BizError(Exception):
    """业务异常，携带业务错误码与提示信息"""

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super().__init__(msg)


def param_error(msg):
    return BizError(Code.PARAM_ERROR, msg)
