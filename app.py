from flask import Flask

from blueprints.ticket import ticket_bp
from config import Config
from exceptions import BizError
from extensions import cors, db
from utils.response import Code, fail


def register_blueprints(app):
    app.register_blueprint(ticket_bp)


def register_error_handlers(app):
    @app.errorhandler(BizError)
    def handle_biz_error(e):
        return fail(e.code, e.msg)

    @app.errorhandler(404)
    def handle_404(e):
        return fail(Code.NOT_FOUND, "接口不存在", http_status=404)

    @app.errorhandler(405)
    def handle_405(e):
        return fail(Code.PARAM_ERROR, "请求方法不允许", http_status=405)

    @app.errorhandler(Exception)
    def handle_exception(e):
        db.session.rollback()
        app.logger.exception("Unhandled exception: %s", e)
        return fail(Code.SERVER_ERROR, "服务器内部错误", http_status=500)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.ensure_ascii = False  # 返回中文不乱码

    db.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": Config.CORS_ORIGINS.split(",")}},
    )

    register_blueprints(app)
    register_error_handlers(app)

    # 演示用：启动时自动建表（生产环境建议使用 Flask-Migrate 管理）
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route("/api/health", methods=["GET"])
def health():
    return success({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
