from flask import Blueprint, request

from extensions import db
from exceptions import BizError, param_error
from models import (
    AlarmTicket,
    ALARM_LEVELS,
    VALID_STATUSES,
)
from utils.pagination import paginate
from utils.response import Code, success
from utils.validators import parse_datetime, parse_int

ticket_bp = Blueprint("ticket", __name__, url_prefix="/api/ticket")


@ticket_bp.route("", methods=["GET"])
def list_tickets():
    """工单列表查询接口：支持分页与多条件筛选"""
    # 分页参数
    page = parse_int(request.args.get("page"), 1, "page", min_value=1)
    page_size = parse_int(
        request.args.get("pageSize"), 10, "pageSize", min_value=1, max_value=100
    )

    # 筛选参数
    alarm_type = request.args.get("alarmType")
    alarm_level = parse_int(
        request.args.get("alarmLevel"), None, "alarmLevel", min_value=1, max_value=4
    )
    cell_id = request.args.get("cellId")
    status = request.args.get("status")
    start_time = parse_datetime(request.args.get("startTime"), "startTime")
    end_time = parse_datetime(request.args.get("endTime"), "endTime")

    # 枚举值校验
    if alarm_level is not None and alarm_level not in ALARM_LEVELS:
        raise param_error("告警级别 alarmLevel 取值必须为 1-4")
    if status is not None and status not in VALID_STATUSES:
        raise param_error(
            "工单状态 status 取值必须为 %s" % "/".join(sorted(VALID_STATUSES))
        )
    if start_time and end_time and start_time > end_time:
        raise param_error("startTime 不能晚于 endTime")

    query = AlarmTicket.query

    if alarm_type:
        query = query.filter(AlarmTicket.alarm_type == alarm_type)
    if alarm_level is not None:
        query = query.filter(AlarmTicket.alarm_level == alarm_level)
    if cell_id:
        query = query.filter(AlarmTicket.cell_id == cell_id)
    if status:
        query = query.filter(AlarmTicket.status == status)
    if start_time:
        query = query.filter(AlarmTicket.occur_time >= start_time)
    if end_time:
        query = query.filter(AlarmTicket.occur_time <= end_time)

    # 默认按创建时间倒序
    query = query.order_by(AlarmTicket.create_time.desc(), AlarmTicket.id.desc())

    return success(paginate(query, page, page_size))


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """根据工单ID查询单条工单详情"""
    ticket = db.session.get(AlarmTicket, ticket_id)
    if not ticket:
        raise BizError(Code.NOT_FOUND, "工单不存在")
    return success(ticket.to_dict())
