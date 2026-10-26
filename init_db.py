"""初始化数据库并写入示例数据，便于测试接口"""
from datetime import datetime, timedelta

from app import app
from extensions import db
from models import (
    AlarmTicket,
    STATUS_CLOSED,
    STATUS_PENDING,
    STATUS_PROCESSING,
    STATUS_RECOVERED,
)


def seed():
    if AlarmTicket.query.count() > 0:
        print("数据库已有数据，跳过示例数据写入")
        return

    now = datetime.now()
    samples = [
        AlarmTicket(
            ticket_no="AT20261026001",
            alarm_type="小区退服",
            alarm_level=1,
            cell_id="CELL-1001",
            alarm_content="小区退服告警，影响业务中断",
            occur_time=now - timedelta(hours=2),
            recover_time=now - timedelta(hours=1),
            status=STATUS_RECOVERED,
            handler="张三",
        ),
        AlarmTicket(
            ticket_no="AT20261026002",
            alarm_type="光模块故障",
            alarm_level=2,
            cell_id="CELL-1002",
            alarm_content="光模块收光功率异常",
            occur_time=now - timedelta(hours=5),
            recover_time=None,
            status=STATUS_PROCESSING,
            handler="李四",
        ),
        AlarmTicket(
            ticket_no="AT20261026003",
            alarm_type="温度过高",
            alarm_level=3,
            cell_id="CELL-1003",
            alarm_content="机柜温度超过阈值",
            occur_time=now - timedelta(hours=8),
            recover_time=None,
            status=STATUS_PENDING,
            handler=None,
        ),
        AlarmTicket(
            ticket_no="AT20261026004",
            alarm_type="小区退服",
            alarm_level=1,
            cell_id="CELL-1001",
            alarm_content="小区退服告警，RRU 链路断开",
            occur_time=now - timedelta(days=1),
            recover_time=now - timedelta(days=1, hours=-1),
            status=STATUS_CLOSED,
            handler="王五",
        ),
    ]
    db.session.add_all(samples)
    db.session.commit()
    print("示例数据写入完成")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed()
