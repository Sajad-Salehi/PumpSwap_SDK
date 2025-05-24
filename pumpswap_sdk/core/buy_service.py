from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # type: ignore
from solders.instruction import Instruction # type: ignore
from spl.token.instructions import create_idempotent_associated_token_account

from solders.keypair import Keypair  # type: ignore
from solders.compute_budget import set_compute_unit_price # type: ignore
from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.config.settings import Settings
from pumpswap_sdk.core.pool_service import get_pumpswap_pair_address
from pumpswap_sdk.core.price_service import get_pumpswap_price
from pumpswap_sdk.utils.constants import *
from pumpswap_sdk.utils.instruction import create_pumpswap_buy_instruction
from pumpswap_sdk.utils.transaction import confirm_transaction, send_transaction
from pumpswap_sdk.utils.wsol import generate_wsol_account_ix 



async def buy_pumpswap_token(mint: str, sol_amount: float, payer_pk: str):

    config = Settings()
    payer = Keypair.from_base58_string(payer_pk)

    mint_pubkey = Pubkey.from_string(mint)
    pair_address = await get_pumpswap_pair_address(mint_pubkey)  

    # Compute purchase amounts
    amount_lamports = int(sol_amount * LAMPORTS_PER_SOL)
    token_price_sol = await get_pumpswap_price(mint_pubkey)
    token_amount = sol_amount / token_price_sol
    max_amount_lamports = int(amount_lamports * (1 + config.buy_slippage))

    try:
        client: AsyncClient = await SolanaClient().get_instance()
    
        wsol_token_account, wsol_ix_list = await generate_wsol_account_ix(payer, max_amount_lamports)

        # Create the buy transaction instruction
        accounts, data = await create_pumpswap_buy_instruction(
            pair_address, payer.pubkey(), mint_pubkey, 
            token_amount, wsol_token_account, max_amount_lamports
        )

        # get instruction objects
        buy_ix = Instruction(PUMP_AMM_PROGRAM_ID, data, accounts)
        token_account_ix = create_idempotent_associated_token_account(
            payer.pubkey(), payer.pubkey(), mint_pubkey
        )

        if config.swap_priority_fee > 0:
            ix = [
            set_compute_unit_price(config.swap_priority_fee),
            wsol_ix_list[0],
            wsol_ix_list[1],
            token_account_ix,
            buy_ix,
            wsol_ix_list[2]
        ]
        else:
            ix = [
            wsol_ix_list[0],
            wsol_ix_list[1],
            token_account_ix,
            buy_ix,
            wsol_ix_list[2]
        ]

        tx_buy = await send_transaction(client, payer, [payer], ix)
        if not tx_buy:
            return {
                "status": False,
                "message": "Transaction Failed",
                "data": None
            }

        # wait for transaction confirmation
        resp = await confirm_transaction(client, tx_buy.value)
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
                "tx_id": tx_buy.value,
                "amount": token_amount,
                "price": token_price_sol
            }
        }

    except Exception as e:
        return  {
                "status": False,
                "message": "Transaction Confirmation Failed",
                "data": None
        }



