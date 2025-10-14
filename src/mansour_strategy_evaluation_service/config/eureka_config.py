import logging
import py_eureka_client.eureka_client as eureka_client
from typing import Optional
import socket

logger = logging.getLogger(__name__)

class EurekaConfig:
    def __init__(
        self,
        eureka_server: str = "http://localhost:8761/eureka",
        app_name: str = "strategy-evaluation-service",
        instance_port: int = 8000,
        instance_host: Optional[str] = None
    ):
        self.eureka_server = eureka_server
        self.app_name = app_name
        self.instance_port = instance_port
        self.instance_host = instance_host or self._get_local_ip()
    
    def _get_local_ip(self) -> str:
        """로컬 IP 주소 가져오기"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def register(self):
        """Eureka 서버에 등록"""
        eureka_client.init(
            eureka_server=self.eureka_server,
            app_name=self.app_name,
            instance_port=self.instance_port,
            instance_host=self.instance_host,
            # 헬스체크 URL (선택사항)
            health_check_url=f"http://{self.instance_host}:{self.instance_port}/health",
            # 상태 페이지 URL (선택사항)
            status_page_url=f"http://{self.instance_host}:{self.instance_port}/info",
            # 갱신 주기 (초)
            renewal_interval_in_secs=30,
            # 만료 시간 (초)
            duration_in_secs=90
        )
        logger.info(f"✅ Registered to Eureka: {self.app_name} at {self.instance_host}:{self.instance_port}")