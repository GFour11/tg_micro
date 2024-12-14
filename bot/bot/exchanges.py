from dataclasses import dataclass


@dataclass
class Exchange:
    enabled: bool = True

exchanges = {
    'Binance': Exchange(),
    'BinanceTest': Exchange(),
    'BinancePaper': Exchange(),
}
