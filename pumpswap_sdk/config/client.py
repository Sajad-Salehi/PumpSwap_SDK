from solana.rpc.async_api import AsyncClient
from pumpswap_sdk.config.settings import Settings

class SolanaClient:

    @staticmethod
    async def get_instance() -> AsyncClient:
        client = AsyncClient(Settings().https_rpc_endpoint)
        return client