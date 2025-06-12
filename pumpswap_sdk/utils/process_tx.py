import json
from pumpswap_sdk.core.pool_service import get_pumpswap_pool_data
from pumpswap_sdk.utils.constants import *
from pumpswap_sdk.utils.pool import PumpPool
from solana.rpc.async_api import AsyncClient
from spl.token.instructions import get_associated_token_address

async def handle_pumpswap_buy_tx(client: AsyncClient, mint: Pubkey, tx_signature):
    tx_data_json = (await client.get_transaction(tx_signature, commitment="confirmed")).to_json()
    tx_data = json.loads(tx_data_json)

    account_keys = tx_data["result"]["transaction"]["message"]["accountKeys"]
    pool_data = await get_pumpswap_pool_data(mint)

    pre_balances = tx_data["result"]["meta"]["preBalances"]
    post_balances = tx_data["result"]["meta"]["postBalances"]
    pre_token_balances = tx_data["result"]["meta"].get("preTokenBalances", [])
    post_token_balances = tx_data["result"]["meta"].get("postTokenBalances", [])

    # Find indexes for base, quote and fee recipient accounts
    if pool_data.base_mint == WSOL_TOKEN_ACCOUNT:
        quote_token_index = account_keys.index(str(pool_data.pool_base_token_account))
        base_token_index = account_keys.index(str(pool_data.pool_quote_token_account))
    else:
        quote_token_index = account_keys.index(str(pool_data.pool_quote_token_account))
        base_token_index = account_keys.index(str(pool_data.pool_base_token_account))

    fee_recipient_ata = get_associated_token_address(FEE_RECIPIENT, pool_data.quote_mint)
    fee_recipient_index = account_keys.index(str(fee_recipient_ata))
    sol_amount = (post_balances[quote_token_index] - pre_balances[quote_token_index]) / LAMPORTS_PER_SOL

    def get_token_amount_change(account_index: int) -> float:
        pre_amt = post_amt = 0
        decimals = 6  # default fallback
        for entry in pre_token_balances:
            if entry["accountIndex"] == account_index:
                pre_amt = float(entry["uiTokenAmount"]["amount"])
                decimals = int(entry["uiTokenAmount"]["decimals"])
        for entry in post_token_balances:
            if entry["accountIndex"] == account_index:
                post_amt = float(entry["uiTokenAmount"]["amount"])
        return (pre_amt - post_amt) / (10 ** decimals)

    
    def get_token_fee_received(account_index: int) -> float:
        pre_amt = post_amt = 0
        decimals = 6
        for entry in pre_token_balances:
            if entry["accountIndex"] == account_index:
                pre_amt = float(entry["uiTokenAmount"]["amount"])
                decimals = int(entry["uiTokenAmount"]["decimals"])
        for entry in post_token_balances:
            if entry["accountIndex"] == account_index:
                post_amt = float(entry["uiTokenAmount"]["amount"])

        return (post_amt - pre_amt) / (10 ** decimals)

    token_amount = get_token_amount_change(base_token_index)

    if pool_data.base_mint == WSOL_TOKEN_ACCOUNT:
        fee_amount = get_token_fee_received(fee_recipient_index)
        token_amount -= fee_amount

    return {
        "sol_amount": round(sol_amount, 9),
        "token_amount": round(token_amount, 6),
    }



async def handle_pumpswap_sell_tx(client: AsyncClient, mint: Pubkey, tx_signature):
    tx_data_json = (await client.get_transaction(tx_signature, commitment="confirmed")).to_json()
    tx_data = json.loads(tx_data_json)

    account_keys = tx_data["result"]["transaction"]["message"]["accountKeys"]
    pool_data = await get_pumpswap_pool_data(mint)

    if pool_data.base_mint == WSOL_TOKEN_ACCOUNT:
        quote_token_index = account_keys.index(str(pool_data.pool_base_token_account))
    else:
        quote_token_index = account_keys.index(str(pool_data.pool_quote_token_account))

    pre_balances = tx_data["result"]["meta"]["preBalances"]
    post_balances = tx_data["result"]["meta"]["postBalances"]

    sol_amount = (pre_balances[quote_token_index] - post_balances[quote_token_index]) / LAMPORTS_PER_SOL

    return {
        "sol_amount": round(sol_amount, 9),
    }