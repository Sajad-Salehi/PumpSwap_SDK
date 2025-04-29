from solders.pubkey import Pubkey  # type: ignore
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import MemcmpOpts
from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.utils import constants
from pumpswap_sdk.utils.pool import PumpPool


async def get_pumpswap_pair_address(mint_address: Pubkey):

    client: AsyncClient = await SolanaClient().get_instance()
    filters = [
        MemcmpOpts(offset=43, bytes=str(mint_address)),  # Matching mint address
        MemcmpOpts(offset=75, bytes=str(constants.WSOL_TOKEN_ACCOUNT))  # Matching WSOL token account
    ]
    
    response = await client.get_program_accounts(
        constants.PUMP_AMM_PROGRAM_ID,
        encoding="base64",  
        filters=filters
    )

    if response.value:
        pools = response.value[0].pubkey 
        return pools
    else:
        return None



async def get_pumpswap_pool_data(mint: Pubkey):

    client: AsyncClient = await SolanaClient.get_instance()
    filters = [
        MemcmpOpts(offset=43, bytes=str(mint)),
        MemcmpOpts(offset=75, bytes=str(constants.WSOL_TOKEN_ACCOUNT)),
    ]

    resp = await client.get_program_accounts(
        constants.PUMP_AMM_PROGRAM_ID, 
        filters=filters, 
        encoding='base64'
    )

    if resp.value:
        account_data = resp.value[0].account.data  # base64 encoded
        binary_data = bytes(account_data)  
        pool_data = PumpPool(binary_data)
        return pool_data
    else:
        raise Exception("No matching pool found")