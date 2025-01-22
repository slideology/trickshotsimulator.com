import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """配置应用的日志系统

    Args:
        app: Flask应用实例

    配置说明：
    - 同时输出到控制台和文件
    - 日志文件按大小轮转
    - 包含时间戳、日志级别和模块信息
    - 不同级别的日志使用不同的处理方式
    """
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 配置文件处理器
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'sprunkr.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # 配置应用日志
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # 配置Werkzeug日志
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)

    return app