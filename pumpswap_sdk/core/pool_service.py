from solders.pubkey import Pubkey  # type: ignore
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import MemcmpOpts
from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.utils import constants
from pumpswap_sdk.utils.pool import PumpPool


async def get_pumpswap_pair_address(mint_address: Pubkey):

    client: AsyncClient = await SolanaClient().get_instance()
    search_orders = [
        (mint_address, constants.WSOL_TOKEN_ACCOUNT),
        (constants.WSOL_TOKEN_ACCOUNT, mint_address)
    ]

    for token_a, token_b in search_orders:
        filters = [
            MemcmpOpts(offset=43, bytes=str(token_a)),
            MemcmpOpts(offset=75, bytes=str(token_b)),
        ]

        response = await client.get_program_accounts(
            constants.PUMP_AMM_PROGRAM_ID,
            filters=filters,
            encoding='base64'
        )

        if response.value:
            pools = response.value[0].pubkey 
            return pools
    raise Exception("No matching pool found")



async def get_pumpswap_pool_data(mint: Pubkey):

    client: AsyncClient = await SolanaClient.get_instance()
    search_orders = [
        (mint, constants.WSOL_TOKEN_ACCOUNT),
        (constants.WSOL_TOKEN_ACCOUNT, mint)
    ]

    for token_a, token_b in search_orders:
        filters = [
            MemcmpOpts(offset=43, bytes=str(token_a)),
            MemcmpOpts(offset=75, bytes=str(token_b)),
        ]

        response = await client.get_program_accounts(
            constants.PUMP_AMM_PROGRAM_ID,
            filters=filters,
            encoding='base64'
        )

        if response.value:
            account_data = response.value[0].account.data  # base64 encoded
            binary_data = bytes(account_data)  
            pool_data = PumpPool(binary_data)
            return pool_data

    raise Exception("No matching pool found")