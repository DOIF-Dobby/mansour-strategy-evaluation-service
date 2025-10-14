import abc
import logging
import random
import requests
import py_eureka_client.eureka_client as eureka_client

from mansour_strategy_evaluation_service.config.env_settings import env

logger = logging.getLogger(__name__)

class BaseApiClient(abc.ABC):
    """
    Eureka에 등록된 다른 마이크로서비스와 통신하는 모든 API 클라이언트의 베이스 클래스
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self._base_url = None # 내부적으로 URL을 캐싱하기 위한 변수

    async def _get_base_url(self) -> str:
        """Eureka에서 서비스의 기본 URL을 조회하고 캐싱합니다."""
        if self._base_url:
            return self._base_url

        logger.debug(f"Discovering '{self.service_name}' from Eureka...")
        try:
            application = await eureka_client.get_application(eureka_server=env.EUREKA_SERVER_URL, app_name=self.service_name)
            
            if not application or not application.instances:
                raise Exception(f"Service '{self.service_name}' not found in Eureka")

            instance = random.choice(application.instances)
            
            protocol = "https" if instance.securePort.enabled else "http"
            host = instance.ipAddr
            port = instance.securePort.port if instance.securePort.enabled else instance.port.port
            
            return f"{protocol}://{host}:{port}"
        except Exception as e:
            self._base_url = None
            raise e
            
    def _handle_request_exception(self, e: requests.RequestException):
        """요청 실패 시 공통 예외 처리 및 URL 캐시 초기화"""
        logger.error(f"🔥 API call to '{self.service_name}' failed: {e}")
        # 서비스 주소가 변경되었을 수 있으므로 URL 캐시를 비웁니다.
        self._base_url = None