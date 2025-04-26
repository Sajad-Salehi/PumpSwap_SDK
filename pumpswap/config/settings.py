from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    """Global settings and bot configurations"""
    wss_rpc_endpoint: str = Field(..., env="WSS_RPC_ENDPOINT")
    https_rpc_endpoint: str = Field(..., env="HTTPS_RPC_ENDPOINT")
    
    buy_slippage: float = Field(0.3, env="BUY_SLIPPAGE")
    sell_slippage: float = Field(0.3, env="SELL_SLIPPAGE")
    swap_priority_fee: int = Field(1_500_000, env="SWAP_PRIORITY_FEE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'