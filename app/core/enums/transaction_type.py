from enum import Enum

class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    CRAFT = "craft"
    TRADE = "trade"
    ADMIN_GIVE = "admin_give"
    DAILY_REWARD = "daily_reward"