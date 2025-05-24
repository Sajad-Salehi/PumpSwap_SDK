from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # type: ignore
from solders.instruction import Instruction # type: ignore
from spl.token.instructions import close_account, CloseAccountParams
from solders.keypair import Keypair  # type: ignore
from solders.compute_budget import set_compute_unit_price # type: ignore

from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.config.settings import Settings
from pumpswap_sdk.core.pool_service import get_pumpswap_pair_address
from pumpswap_sdk.core.price_service import get_pumpswap_price
from pumpswap_sdk.utils.constants import *
from pumpswap_sdk.utils.instruction import create_pumpswap_sell_instruction
from pumpswap_sdk.utils.token_account import fetch_token_account
from pumpswap_sdk.utils.transaction import confirm_transaction, send_transaction



async def sell_pumpswap_token(mint: str, token_amount: float, payer_pk: str):

    config = Settings()
    payer = Keypair.from_base58_string(payer_pk)

    mint_pubkey = Pubkey.from_string(mint)
    pair_address = await get_pumpswap_pair_address(mint_pubkey)  
    token_price_sol = await get_pumpswap_price(mint_pubkey)

    # Compute purchase amounts
    slippage_factor = 1 - config.sell_slippage
    min_sol_output = token_amount * token_price_sol
    min_sol_output_lamports = int(min_sol_output * slippage_factor * LAMPORTS_PER_SOL)

    try:
        client: AsyncClient = await SolanaClient().get_instance()
        wsol_token_account, wsol_token_account_instructions = await fetch_token_account(
            payer.pubkey(),
            WSOL_TOKEN_ACCOUNT
        )

        # Create the buy transaction instruction
        accounts, data = await create_pumpswap_sell_instruction(
            pair_address, payer.pubkey(), mint_pubkey, 
            token_amount, wsol_token_account, min_sol_output_lamports
        )

        # get instruction objects
        sell_ix = Instruction(PUMP_AMM_PROGRAM_ID, data, accounts)
        
        close_account_instructions = close_account(
            CloseAccountParams(
                TOKEN_PROGRAM_ID, wsol_token_account, payer.pubkey(), payer.pubkey()
            )
        )
        ix = []

        if config.swap_priority_fee > 0:
            ix = [set_compute_unit_price(config.swap_priority_fee)]
        if wsol_token_account_instructions:
            ix.append(wsol_token_account_instructions)
        ix.append(sell_ix)
        ix.append(close_account_instructions)


        tx_sell = await send_transaction(client, payer, [payer], ix)
        if not tx_sell:
            return {
                "status": False,
                "message": "Transaction Failed",
                "data": None
            }

        # wait for transaction confirmation
        resp = await confirm_transaction(client, tx_sell.value)
        if not resp.value or not resp.value[0] or resp.value[0].err:
            return {
                "status": False,
                "message": f"Transaction Confirmation Failed {resp}",
                "data": None
            }

        return {
                    "status": True,
                    "message": "Transaction completed successfully",
                    "data": {
                        "tx_id": tx_sell.value,
                        "amount": token_amount,
                        "price": token_price_sol
                    }
                }

    except Exception as e:
        return  {
                "status": False,
                "message": f"Transaction Confirmation Failed {e}",
                "data": None
        }



