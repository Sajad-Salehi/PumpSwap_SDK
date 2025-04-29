from solders.pubkey import Pubkey  # type: ignore
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TokenAccountOpts
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from pumpswap_sdk.config.client import SolanaClient


async def fetch_token_account(owner: Pubkey, mint: Pubkey):
    try:
        client: AsyncClient = await SolanaClient().get_instance()
        account_data = await client.get_token_accounts_by_owner(owner, TokenAccountOpts(mint=mint))
        
        if account_data.value:
            token_account = account_data.value[0].pubkey
            token_account_instructions = None
        else:
            token_account = get_associated_token_address(owner, mint)
            token_account_instructions = create_associated_token_account(owner, owner, mint)

        return token_account, token_account_instructions

    except Exception as e:
        return None, None