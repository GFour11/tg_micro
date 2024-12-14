import time

from typing import Callable, Union
from datetime import datetime

from microservice_core.microservices import MicroserviceClient
from microservice_core.messages.message import Message, Header
from microservice_core.messages.kline_stream import KlineStreamRequestBody


class AbstractStreamClient(MicroserviceClient):
    def __init__(self, host: str, port: int):
        super().__init__(host=host, port=port)
        self.subscribed: bool = False

    # TODO: Delete test_mode
    def subscribe(
            self,
            exchange: str,
            symbol: str,
            callback: Callable[[str], None],
            return_data: Union[set, None] = None,
            test_mode: bool = True):
        """
        Subscribes to stream data for a specific symbol on a specific exchange.

        Parameters:
            :param exchange: Which exchange will be connected to.
            :param symbol: Which symbol to subscribe to.
            :param callback: Which callback should be called after receiving data from a stream.
            :param return_data: What data should be returned. Default value is None,
                                this means that all received data will be returned.
            :param test_mode:
        """
        start_time = time.time()
        if self.subscribed:
            raise RuntimeError(f"Client is already subscribed to the stream")
        self.subscribed = True
        self.connect()

        header = Header(
            message_type='REQUEST',
            command='subscribe',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        body = KlineStreamRequestBody(
            exchange=exchange,
            symbol=symbol,
            return_data=return_data
        )

        message = Message(header=header, body=body)

        self.send(message)

        if test_mode:
            while True:
                msg = self.receive()
                if msg is None:  # TODO: Test and remove this logic
                    break
                callback(msg)
                if time.time() - start_time > 10:
                    self.unsubscribe()
        else:
            while True:
                msg = self.receive()
                if msg is None:  # TODO: Test and remove this logic
                    break
                callback(msg)
        self.subscribed = False

    def unsubscribe(self):
        """Unsubscribes from the stream data."""
        if not self.subscribed:
            raise RuntimeError(f"Client is not yet subscribed to the stream")
        self.subscribed = False
        self.disconnect()


class KlineStreamClient(AbstractStreamClient):
    def __init__(self, host: str, port: int = 5000):
        super().__init__(host, port)
