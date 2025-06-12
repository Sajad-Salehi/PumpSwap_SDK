import struct
from solders.pubkey import Pubkey  # type: ignore
from solders.instruction import AccountMeta  # type: ignore
from spl.token.instructions import get_associated_token_address
from pumpswap_sdk.core.pool_service import get_pumpswap_pool_data
from pumpswap_sdk.utils.constants import *
from pumpswap_sdk.utils.pool import PumpPool



async def create_pumpswap_buy_instruction(pool_data: PumpPool, pool_id: Pubkey, user: Pubkey, mint: Pubkey, token_amount: float, wsol_token_account: Pubkey, max_amount_lamports: int):
    
    if pool_data.base_mint == WSOL_TOKEN_ACCOUNT:
        user_base_token_account = wsol_token_account
        user_quote_token_account = get_associated_token_address(user, mint)
        data = (
            SELL_DISCRIMINATOR
            + struct.pack("<Q", max_amount_lamports)  # Max lamports allowed for the transaction
            + struct.pack("<Q", int(token_amount * TOKEN_DECIMALS))  # Convert token amount to smallest unit
        )
    
    else:
        user_base_token_account = get_associated_token_address(user, mint)
        user_quote_token_account = wsol_token_account
        data = (
            BUY_DISCRIMINATOR
            + struct.pack("<Q", int(token_amount * TOKEN_DECIMALS))  # Convert token amount to smallest unit
            + struct.pack("<Q", max_amount_lamports)  # Max lamports allowed for the transaction
        )

    pool_base_token_account = pool_data.pool_base_token_account
    pool_quote_token_account = pool_data.pool_quote_token_account

    vault_auth_seeds = [b"creator_vault", bytes(pool_data.coin_creator)]
    vault_auth_pda, _ = Pubkey.find_program_address(vault_auth_seeds, PUMP_AMM_PROGRAM_ID)
    vault_ata = get_associated_token_address(vault_auth_pda, pool_data.quote_mint)
    fee_recipient_ata = get_associated_token_address(FEE_RECIPIENT, pool_data.quote_mint)

    accounts = [
        AccountMeta(pubkey=pool_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=user, is_signer=True, is_writable=True),
        AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
        AccountMeta(pubkey=pool_data.base_mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=pool_data.quote_mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=user_base_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=user_quote_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=pool_base_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=pool_quote_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=fee_recipient_ata, is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
        AccountMeta(pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(pubkey=PUMP_AMM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=vault_ata, is_signer=False, is_writable=True),
        AccountMeta(pubkey=vault_auth_pda, is_signer=False, is_writable=False),
    ]
    
    return accounts, data




async def create_pumpswap_sell_instruction(pool_data: PumpPool, pool_id: Pubkey, user: Pubkey, token_amount: int, quote_account: Pubkey, min_sol_lamports: int):
    
    if pool_data.base_mint == WSOL_TOKEN_ACCOUNT:
        data = (
            BUY_DISCRIMINATOR
            + struct.pack("<Q", int(min_sol_lamports))
            + struct.pack("<Q", int(token_amount * TOKEN_DECIMALS))
        )
        print(min_sol_lamports, token_amount)
    
    else:
        data = (
            SELL_DISCRIMINATOR
            + struct.pack("<Q", int(token_amount * TOKEN_DECIMALS))
            + struct.pack("<Q", int(min_sol_lamports))
        )


    user_base_token_account = get_associated_token_address(user, pool_data.base_mint)
    user_quote_token_account =  get_associated_token_address(user, pool_data.quote_mint)

    pool_base_token_account = pool_data.pool_base_token_account
    pool_quote_token_account = pool_data.pool_quote_token_account

    vault_auth_seeds = [b"creator_vault", bytes(pool_data.coin_creator)]
    vault_auth_pda, _ = Pubkey.find_program_address(vault_auth_seeds, PUMP_AMM_PROGRAM_ID)
    vault_ata = get_associated_token_address(vault_auth_pda, pool_data.quote_mint)
    fee_recipient_ata = get_associated_token_address(FEE_RECIPIENT, pool_data.quote_mint)

    accounts = [
        AccountMeta(pubkey=pool_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=user, is_signer=True, is_writable=True),
        AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
        AccountMeta(pubkey=pool_data.base_mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=pool_data.quote_mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=user_base_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=user_quote_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=pool_base_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=pool_quote_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=fee_recipient_ata, is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
        AccountMeta(pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(pubkey=PUMP_AMM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=vault_ata, is_signer=False, is_writable=True),
        AccountMeta(pubkey=vault_auth_pda, is_signer=False, is_writable=False),
    ]
   
    return accounts, data