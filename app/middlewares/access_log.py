# app/middlewares/access_log.py
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.access")


class JSONLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "access",
            extra={
                "client_ip": request.client.host if request.client else None,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.url.query),
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response