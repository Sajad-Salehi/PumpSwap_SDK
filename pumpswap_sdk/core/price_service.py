from solders.pubkey import Pubkey  # type: ignore
from solana.rpc.async_api import AsyncClient

from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.core.pool_service import get_pumpswap_pool_data
from pumpswap_sdk.utils.pool import PumpPool



async def get_pumpswap_price(mint_address: Pubkey):

    client: AsyncClient = await SolanaClient().get_instance()
    data: PumpPool = await get_pumpswap_pool_data(mint_address)

    qoute_balance = await client.get_token_account_balance(data.pool_quote_token_account)
    base_balance = await client.get_token_account_balance(data.pool_base_token_account)

    price = qoute_balance.value.ui_amount / base_balance.value.ui_amount
    return price