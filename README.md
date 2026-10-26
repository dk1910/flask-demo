# 告警工单查询后端

基于 Python Flask + SQLAlchemy 的告警工单查询接口。

## 功能

- 工单列表查询：分页 + 按告警类型 / 告警级别 / 小区ID / 工单状态 / 时间范围筛选
- 工单单条详情查询
- 统一 JSON 返回格式 `{code, msg, data}`
- 参数校验、全局异常处理、跨域 CORS 支持

## 安装运行

```bash
cd alarm_ticket_api
pip install -r requirements.txt

# 初始化数据库并写入示例数据
python init_db.py

# 启动服务
python app.py
```

服务默认监听 `http://127.0.0.1:5000`。

## 返回码说明

| code  | 含义           |
|-------|----------------|
| 0     | 成功           |
| 40001 | 参数校验失败   |
| 40401 | 资源不存在     |
| 50000 | 服务器内部错误 |

## 字段说明

| 字段        | 说明                          |
|-------------|-------------------------------|
| alarmLevel  | 1-紧急 2-重要 3-次要 4-提示  |
| status      | pending / processing / recovered / closed |

## 接口调用示例

### 1. 工单列表查询

```bash
# 基础分页查询
curl "http://127.0.0.1:5000/api/ticket?page=1&pageSize=10"

# 多条件筛选：告警类型=小区退服，级别=1，状态=recovered
curl "http://127.0.0.1:5000/api/ticket?alarmType=小区退服&alarmLevel=1&status=recovered"

# 按小区ID + 时间范围筛选
curl "http://127.0.0.1:5000/api/ticket?cellId=CELL-1001&startTime=2026-10-25 00:00:00&endTime=2026-10-26 23:59:59"
```

返回示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total": 1,
    "page": 1,
    "pageSize": 10,
    "pages": 1,
    "items": [
      {
        "id": 1,
        "ticketNo": "AT20261026001",
        "alarmType": "小区退服",
        "alarmLevel": 1,
        "alarmLevelDesc": "紧急",
        "cellId": "CELL-1001",
        "alarmContent": "小区退服告警，影响业务中断",
        "occurTime": "2026-10-26 12:00:00",
        "recoverTime": "2026-10-26 13:00:00",
        "status": "recovered",
        "handler": "张三",
        "createTime": "2026-10-26 14:00:00"
      }
    ]
  }
}
```

### 2. 工单详情查询

```bash
curl "http://127.0.0.1:5000/api/ticket/1"
```

返回示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": 1,
    "ticketNo": "AT20261026001",
    "alarmType": "小区退服",
    "alarmLevel": 1,
    "alarmLevelDesc": "紧急",
    "cellId": "CELL-1001",
    "alarmContent": "小区退服告警，影响业务中断",
    "occurTime": "2026-10-26 12:00:00",
    "recoverTime": "2026-10-26 13:00:00",
    "status": "recovered",
    "handler": "张三",
    "createTime": "2026-10-26 14:00:00"
  }
}
```

### 3. 错误示例

```bash
# 参数校验失败：page 非整数
curl "http://127.0.0.1:5000/api/ticket?page=abc"
# {"code": 40001, "msg": "参数 page 必须为整数", "data": null}

# 工单不存在
curl "http://127.0.0.1:5000/api/ticket/9999"
# {"code": 40401, "msg": "工单不存在", "data": null}
```

## 项目结构

```
alarm_ticket_api/
├── app.py                 # 应用入口、蓝图注册、全局异常处理
├── config.py              # 配置
├── extensions.py          # db / cors 扩展实例
├── models.py              # 工单模型、常量定义
├── exceptions.py          # 自定义业务异常
├── init_db.py             # 建表 + 示例数据
├── requirements.txt       # 依赖
├── utils/
│   ├── response.py        # 统一响应
│   ├── pagination.py      # 分页工具
│   └── validators.py      # 参数校验
└── blueprints/
    └── ticket.py          # 工单路由
```
