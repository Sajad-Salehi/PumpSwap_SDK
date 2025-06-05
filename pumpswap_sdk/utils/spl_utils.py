from solders.instruction import Instruction #type: ignore
from solders.pubkey import Pubkey  #type: ignore
from solders.keypair import Keypair  #type: ignore

import spl.token.instructions as spl_token
from pumpswap_sdk.utils.constants import *


def close_associated_token_account(owner: Keypair, associated_account_address: Pubkey) -> Instruction:
    return (spl_token.close_account(spl_token.CloseAccountParams(
        program_id=TOKEN_PROGRAM_ID,
            account=associated_account_address,
            dest=owner.pubkey(),
            owner=owner.pubkey()
    )))


