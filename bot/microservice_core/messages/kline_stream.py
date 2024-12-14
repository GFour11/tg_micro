from typing import Union

from dataclasses import dataclass
from typing import Any
from .message import AbstractRequestBody, AbstractResponseBody


@dataclass
class KlineStreamRequestBody(AbstractRequestBody):
    exchange: str
    symbol: str
    return_data: set or None


@dataclass
class KlineStreamResponseBody(AbstractResponseBody):
    event_type: Union[str, None] = None
    event_time: Union[int, None] = None
    symbol: Union[str, None] = None
    start_time: Union[int, None] = None
    close_time: Union[int, None] = None
    interval: Union[str, None] = None
    first_trade_id: Union[int, None] = None
    last_trade_id: Union[int, None] = None
    open_price: Union[str, None] = None
    close_price: Union[str, None] = None
    high_price: Union[str, None] = None
    low_price: Union[str, None] = None
    base_asset_volume: Union[str, None] = None
    number_of_trades: Union[int, None] = None
    is_closed: Union[bool, None] = None
    quote_asset_volume: Union[str, None] = None
    taker_buy_base_asset_volume: Union[str, None] = None
    taker_buy_quote_asset_volume: Union[str, None] = None

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data['status']
        return {
            "status": self.status,
            "return_data": data
        }
