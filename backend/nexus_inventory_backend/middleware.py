import time
import logging

logger = logging.getLogger(__name__)


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.info(
            f"request: {request.method} {request.path} {response.status_code} {duration:.3f}s"
        )

        return response
