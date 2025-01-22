import os
import logging
import sys

def setup_logging(app):
    """配置应用的日志系统

    Args:
        app: Flask应用实例

    配置说明：
    - 在开发环境输出到控制台和文件
    - 在生产环境仅输出到控制台
    - 包含时间戳、日志级别和模块信息
    """
    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 配置控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 配置应用日志
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)

    # 配置Werkzeug日志
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(console_handler)

    # 在开发环境中添加文件日志
    if app.debug:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(os.path.join(log_dir, 'sprunkr.log'))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        app.logger.addHandler(file_handler)
        werkzeug_logger.addHandler(file_handler)

    return app