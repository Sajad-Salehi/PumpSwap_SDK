from pumpswap_sdk.core.buy_service import buy_pumpswap_token
from pumpswap_sdk.core.sell_service import sell_pumpswap_token
from pumpswap_sdk.core.pool_service import get_pumpswap_pair_address, get_pumpswap_pool_data
from pumpswap_sdk.core.price_service import get_pumpswap_price
from pumpswap_sdk.sdk.models import Constants, Models
from pumpswap_sdk.utils.instruction import create_pumpswap_buy_instruction, create_pumpswap_sell_instruction
from solders.pubkey import Pubkey  # type: ignore


class PumpSwapSDK:

    def __init__(self):
        self.constants = Constants()
        self.models = Models()


    async def buy(self, mint:str, sol_amount: float, payer_pk: str):
        return (await buy_pumpswap_token(mint, sol_amount, payer_pk))


    async def sell(self, mint:str, token_amount: float, payer_pk: str):
        return (await sell_pumpswap_token(mint, token_amount, payer_pk))
    

    async def get_pair_address(self, mint_address: str):
        mint_pubkey = Pubkey.from_string(mint_address)
        return (await get_pumpswap_pair_address(mint_pubkey))
    

    async def get_pool_data(self, mint_address: str):
        mint_pubkey = Pubkey.from_string(mint_address)
        return (await get_pumpswap_pool_data(mint_pubkey))
    

    async def get_token_price(self, pair_address: str):
        return (await get_pumpswap_price(pair_address))
    

    async def create_buy_instruction(self, pool_id: Pubkey, user: Pubkey, mint: Pubkey, token_amount: float, quote_account: Pubkey, max_amount_lamports: int):
        return await create_pumpswap_buy_instruction(pool_id, user, mint, token_amount, quote_account, max_amount_lamports)


    async def create_sell_instruction(self, pool_id: Pubkey, user: Pubkey, mint: Pubkey, token_amount: float, quote_account: Pubkey, min_sol_lamports: int):
        return await create_pumpswap_sell_instruction(pool_id, user, mint, token_amount, quote_account, min_sol_lamports)

