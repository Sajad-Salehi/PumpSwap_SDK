from construct import Struct, Int8ul, Int16ul, Int64ul, Bytes
from solders.pubkey import Pubkey #type: ignore

class PumpPool:
    _STRUCT = Struct(
        "pool_bump" / Int8ul,
        "index" / Int16ul,
        "creator" / Bytes(32),
        "base_mint" / Bytes(32),
        "quote_mint" / Bytes(32),
        "lp_mint" / Bytes(32),
        "pool_base_token_account" / Bytes(32),
        "pool_quote_token_account" / Bytes(32),
        "lp_supply" / Int64ul,
        "coin_creator" / Bytes(32),
    )

    def __init__(self, data: bytes) -> None:
        parsed = self._STRUCT.parse(data[8:243])
        self.pool_bump = parsed.pool_bump
        self.index = parsed.index
        self.creator = Pubkey.from_bytes(parsed.creator)
        self.base_mint = Pubkey.from_bytes(parsed.base_mint)
        self.quote_mint = Pubkey.from_bytes(parsed.quote_mint)
        self.lp_mint = Pubkey.from_bytes(parsed.lp_mint)
        self.pool_base_token_account = Pubkey.from_bytes(parsed.pool_base_token_account)
        self.pool_quote_token_account = Pubkey.from_bytes(parsed.pool_quote_token_account)
        self.lp_supply = parsed.lp_supply
        self.coin_creator = Pubkey.from_bytes(parsed.coin_creator)
