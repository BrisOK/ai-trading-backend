from pydantic import BaseModel
from datetime import datetime

# ... existing schemas ...


class SignalRequest(BaseModel):
        symbol: str
        market: str = "stock"    # "stock" or "crypto"