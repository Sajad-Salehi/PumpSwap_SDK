from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey # type: ignore
from pumpswap_sdk.config.client import SolanaClient
from spl.token.instructions import get_associated_token_address


async def get_sol_balance(address: Pubkey) -> float:
    try:
        client: AsyncClient = await SolanaClient().get_instance()
        response = await client.get_balance(address)
        return float(response.value) / (10 ** 9)

    except Exception as e:
        return 0.0


async def get_spl_token_balance(address: Pubkey) -> float:
    try:
        client: AsyncClient = await SolanaClient().get_instance()
        response = await client.get_token_account_balance(address)
        return float(response.value.amount) / (10 ** 6)
    
    except Exception as e:
        return 0.0


async def get_wallet_spl_token_balance(address: Pubkey, mint: Pubkey) -> float:
    try:
        client: AsyncClient = await SolanaClient().get_instance()
        token_acc = get_associated_token_address(address, mint)
        response = await client.get_token_account_balance(token_acc, commitment="processed")
        return float(response.value.amount) / (10 ** 6)
    
    except Exception as e:
        return 0.0