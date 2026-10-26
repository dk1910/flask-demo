from datetime import datetime

from extensions import db

# 告警级别
ALARM_LEVELS = {1, 2, 3, 4}
ALARM_LEVEL_MAP = {1: "紧急", 2: "重要", 3: "次要", 4: "提示"}

# 工单状态
STATUS_PENDING = "pending"          # 待处理
STATUS_PROCESSING = "processing"    # 处理中
STATUS_RECOVERED = "recovered"      # 已恢复
STATUS_CLOSED = "closed"            # 已关闭
VALID_STATUSES = {STATUS_PENDING, STATUS_PROCESSING, STATUS_RECOVERED, STATUS_CLOSED}


def _fmt(dt):
    """将 datetime 格式化为字符串，空值返回 None"""
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None


class AlarmTicket(db.Model):
    """告警工单表"""
    __tablename__ = "alarm_ticket"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="工单id")
    ticket_no = db.Column(db.String(64), unique=True, nullable=False, index=True, comment="工单编号")
    alarm_type = db.Column(db.String(64), nullable=False, index=True, comment="告警类型")
    alarm_level = db.Column(db.Integer, nullable=False, index=True, comment="告警级别 1-紧急 2-重要 3-次要 4-提示")
    cell_id = db.Column(db.String(64), nullable=False, index=True, comment="小区ID")
    alarm_content = db.Column(db.Text, nullable=False, comment="告警内容")
    occur_time = db.Column(db.DateTime, nullable=False, index=True, comment="发生时间")
    recover_time = db.Column(db.DateTime, nullable=True, comment="恢复时间")
    status = db.Column(db.String(32), nullable=False, default=STATUS_PENDING, index=True, comment="工单状态")
    handler = db.Column(db.String(64), nullable=True, comment="处理人")
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="创建时间")

    def to_dict(self):
        return {
            "id": self.id,
            "ticketNo": self.ticket_no,
            "alarmType": self.alarm_type,
            "alarmLevel": self.alarm_level,
            "alarmLevelDesc": ALARM_LEVEL_MAP.get(self.alarm_level),
            "cellId": self.cell_id,
            "alarmContent": self.alarm_content,
            "occurTime": _fmt(self.occur_time),
            "recoverTime": _fmt(self.recover_time),
            "status": self.status,
            "handler": self.handler,
            "createTime": _fmt(self.create_time),
        }
