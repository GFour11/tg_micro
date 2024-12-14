from microservice_core.messages.message import dataclass, AbstractRequestBody, AbstractResponseBody, ErrorBody

from typing import Optional, Dict, Any

@dataclass
class UsersRequestBody(AbstractRequestBody):
    user_id: Optional[int] = None
    user_data: Optional[Dict[str, str]] = None
    referral_code: Optional[str] = None
    key_id: Optional[int] = None
    key_data: Optional[Dict[str, Any]] = None


@dataclass
class UsersResponseBody(AbstractResponseBody):
    message: Optional[Any] = None
    error: Optional[ErrorBody] = None
    status: str = "success"

