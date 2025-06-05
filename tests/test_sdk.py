import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, AsyncMock
from pumpswap_sdk import PumpSwapSDK


mint = "your-token-mint"  # Replace with a valid mint address on pumpswap
user_private_key = "your-private-key"  # Replace with a valid private key
sol_amount = 0.0001 # Example SOL amount to buy


@pytest.mark.asyncio
async def test_buy_and_sell():
    sdk = PumpSwapSDK()

    # Perform a real buy
    buy_result = await sdk.buy(mint, sol_amount, user_private_key)
    print(f"Buy result: {buy_result}")

    assert buy_result["status"] is True

    # Extract the token amount actually received
    token_amount = buy_result["data"]["token_amount"]

    # Now sell that exact amount
    sell_result = await sdk.sell(mint, token_amount, user_private_key)
    print(f"Sell result: {sell_result}")

    assert sell_result["status"] is True