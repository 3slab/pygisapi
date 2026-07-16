# app/logging_config.py
import logging
import json
from datetime import datetime, timezone

# Champs standards de LogRecord à exclure du "extra"
STANDARD_FIELDS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process", "message", "taskName",
}


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
        }

        # Ajoute les champs "extra" (client_ip, method, path, etc.)
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in STANDARD_FIELDS
        }

        if extra_fields:
            log_entry.update(extra_fields)
        else:
            log_entry["message"] = record.getMessage()

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)

    logging.getLogger("uvicorn.error").handlers = [handler]
    logging.getLogger("uvicorn.error").propagate = False

    logging.getLogger("uvicorn.access").disabled = True