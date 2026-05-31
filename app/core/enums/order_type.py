from enum import Enum

class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(str, Enum):
    OPEN = "open"
    FILLED = "filled"
    CANCELLED = "cancelled"
    PARTIALLY_FILLED = "partially_filled"