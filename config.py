import os


class Config:
    """应用配置"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # 数据库连接，默认使用 SQLite，可通过环境变量 DATABASE_URL 切换为 MySQL/PostgreSQL 等
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///alarm_ticket.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS 允许的来源，逗号分隔，默认全部放开
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
