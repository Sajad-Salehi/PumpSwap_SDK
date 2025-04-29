
from pumpswap_sdk.utils.constants import *
from pumpswap_sdk.utils.pool import PumpPool


class Models:
    def __init__(self):
        self.PumpPool = PumpPool


class Constants:
    def __init__(self):
        self.LAMPORTS_PER_SOL = LAMPORTS_PER_SOL
        self.TOKEN_DECIMALS = TOKEN_DECIMALS
        self.WSOL_TOKEN_ACCOUNT = WSOL_TOKEN_ACCOUNT
        self.PUMP_AMM_PROGRAM_ID = PUMP_AMM_PROGRAM_ID
        self.ASSOCIATED_TOKEN_PROGRAM_ID = ASSOCIATED_TOKEN_PROGRAM_ID
        self.TOKEN_PROGRAM_ID = TOKEN_PROGRAM_ID
        self.FEE_RECIPIENT = FEE_RECIPIENT
        self.FEE_RECIPIENT_ATA = FEE_RECIPIENT_ATA
        self.EVENT_AUTHORITY = EVENT_AUTHORITY
        self.GLOBAL = GLOBAL
        self.SYSTEM_PROGRAM = SYSTEM_PROGRAM
        self.BUY_DISCRIMINATOR = BUY_DISCRIMINATOR
        self.SELL_DISCRIMINATOR = SELL_DISCRIMINATOR