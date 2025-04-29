import base64
import os
from solders.pubkey import Pubkey  # type: ignore
from spl.token.async_client import AsyncToken

from solders.keypair import Keypair #type: ignore
from solana.rpc.async_api import AsyncClient
from solders.system_program import (
    CreateAccountWithSeedParams,
    create_account_with_seed,
)
from spl.token.instructions import (
    CloseAccountParams,
    InitializeAccountParams,
    close_account,
    initialize_account,
)

from pumpswap_sdk.config.client import SolanaClient
from pumpswap_sdk.utils.constants import *

async def generate_wsol_account_ix(payer: Keypair, amount_lamports):

    client: AsyncClient = await SolanaClient().get_instance()

    seed = base64.urlsafe_b64encode(os.urandom(24)).decode("utf-8")
    wsol_token_account = Pubkey.create_with_seed(payer.pubkey(), seed, TOKEN_PROGRAM_ID)
    balance_needed = await AsyncToken.get_min_balance_rent_for_exempt_for_account(client)

    create_wsol_account_instruction = create_account_with_seed(
        CreateAccountWithSeedParams(
            from_pubkey=payer.pubkey(),
            to_pubkey=wsol_token_account,
            base=payer.pubkey(),
            seed=seed,
            lamports=int(balance_needed + amount_lamports + 1000000),
            space=165,
            owner=TOKEN_PROGRAM_ID,
        )
    )

    init_wsol_account_instruction = initialize_account(
        InitializeAccountParams(
            program_id=TOKEN_PROGRAM_ID,
            account=wsol_token_account,
            mint=WSOL_TOKEN_ACCOUNT,
            owner=payer.pubkey(),
        )
    )

    close_wsol_account_instruction = close_account(
        CloseAccountParams(
            program_id=TOKEN_PROGRAM_ID,
            account=wsol_token_account,
            dest=payer.pubkey(),
            owner=payer.pubkey(),
        )
    )

    return wsol_token_account, [
        create_wsol_account_instruction, 
        init_wsol_account_instruction, 
        close_wsol_account_instruction
    ]
