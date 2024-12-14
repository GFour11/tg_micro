from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from microservice_core.messages.message import AbstractResponseBody, ErrorBody

@dataclass
class UsersResponseBody(AbstractResponseBody):
    message: Optional[Any] = None
    error: Optional[ErrorBody] = None
    status: str = "success"
