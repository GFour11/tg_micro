from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Header:
    message_type: str  # REQUEST, RESPONSE
    command: str
    timestamp: str


@dataclass
class AbstractRequestBody(ABC):
    def to_dict(self) -> dict[str, Any]:
        # noinspection PyTypeChecker
        return asdict(self)


@dataclass
class AbstractResponseBody:
    status: str

    def to_dict(self) -> dict[str, Any]:
        # noinspection PyTypeChecker
        return asdict(self)


@dataclass
class ErrorBody:
    error_code: str
    error_message: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        # noinspection PyTypeChecker
        return asdict(self)


@dataclass
class Message:
    header: Header
    body: Any

    def to_dict(self) -> dict[str, Any]:
        # noinspection PyTypeChecker
        return asdict(self)
