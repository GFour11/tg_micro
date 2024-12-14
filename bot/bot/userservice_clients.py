from typing import Callable, Optional, Dict, Any
from datetime import datetime
from microservice_core.microservices import MicroserviceClient
from microservice_core.messages.message import Message, Header
from .custom_classes import UsersRequestBody

class UserMicroserviceClient(MicroserviceClient):
    def __init__(self, host: str, port: int = 5000):
        super().__init__(host=host, port=port)

    def send_user_data(self, command: str, user_id: Optional[int] = None,
                       user_data: Optional[Dict[str, str]] = None,
                       referral_code: Optional[str] = None,
                       key_id: Optional[int] = None,
                       key_data: Optional[Dict[str, Any]] = None) -> Any:

        self.connect()

        header = Header(
            message_type='REQUEST',
            command=command,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        body = UsersRequestBody(
            user_id=user_id,
            user_data=user_data,
            referral_code=referral_code,
            key_id=key_id,
            key_data=key_data
        )

        message = Message(header=header, body=body)

        self.send(message.to_dict())

        response = self.receive()
        self.disconnect()

        return response

    def subscribe(self, command: str, callback: Callable[[Any], None]):

        self.connect()

        header = Header(
            message_type='REQUEST',
            command=command,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        body = {}

        message = Message(header=header, body=body)
        self.send(message.to_dict())

        while True:
            msg = self.receive()
            if msg is None:
                break
            callback(msg)

        self.disconnect()
