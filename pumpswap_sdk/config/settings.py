from pydantic import Field
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Global settings and bot configurations"""
    https_rpc_endpoint: str = Field("https://api.mainnet-beta.solana.com", env="HTTPS_RPC_ENDPOINT")
    buy_slippage: float = Field(0.3, env="BUY_SLIPPAGE")
    sell_slippage: float = Field(0.3, env="SELL_SLIPPAGE")
    swap_priority_fee: int = Field(1_500_000, env="SWAP_PRIORITY_FEE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"