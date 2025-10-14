import os
import yaml
import logging.config

def setup_logging():
    """YAML 기반 로깅 설정"""
    log_target = os.getenv("LOG_TARGET", "console")
    targets = [t.strip() for t in log_target.split(",")]

    # YAML 설정 파일 경로
    config_path = os.path.join(os.path.dirname(__file__), "logging.yaml")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # handlers와 root.handler를 동적으로 채움
    available_handlers = config.get("handlers", {})
    root_handlers = []
    replace_handlers = {}

    if "console" in targets and "console" in available_handlers:
        root_handlers.append("console")
        console_handler = available_handlers.get('console')
        replace_handlers['console'] = console_handler

    if "file" in targets and "file" in available_handlers:
        os.makedirs("logs", exist_ok=True)  # 로그 폴더 생성
        root_handlers.append("file")
        file_handler = available_handlers.get('file')
        replace_handlers['file'] = file_handler

    config["root"]["handlers"] = root_handlers
    config['handlers'] = replace_handlers

    logging.config.dictConfig(config)
    
    # 특정 라이브러리의 로그 레벨 조정
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("kafka").setLevel(logging.WARNING)
    logging.getLogger("py_eureka_client").setLevel(logging.WARNING)
    
    return logging.getLogger()

def get_logger(name: str) -> logging.Logger:
    """특정 모듈용 로거 가져오기"""
    return logging.getLogger(name)
