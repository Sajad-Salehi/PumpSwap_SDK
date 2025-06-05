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

    # Mock buy_pumpswap_token
    with patch('pumpswap_sdk.core.buy_service.buy_pumpswap_token', new_callable=AsyncMock) as mock_buy:
        mock_buy.return_value = {
            "status": True,
            "message": "Transaction completed successfully",
            "data": {
                "token_amount": 63.460034,  # example result from buy
                "sol_amount": sol_amount,
                "tx_id": "mocked_tx_id",
            }
        }

        # Call the SDK buy method
        buy_result = await sdk.buy(mint, sol_amount, user_private_key)
        print(f"Buy result: {buy_result}")

        assert buy_result["status"] is True
        assert buy_result["message"] == "Transaction completed successfully"

        # Extract the exact token amount received from buy
        bought_token_amount = buy_result["data"]["token_amount"]

    # Mock sell_pumpswap_token
    with patch('pumpswap_sdk.core.sell_service.sell_pumpswap_token', new_callable=AsyncMock) as mock_sell:
        mock_sell.return_value = {
            "status": True,
            "message": "Transaction completed successfully",
            "data": {
                "token_amount": bought_token_amount,
                "sol_amount": sol_amount,
                "tx_id": "mocked_sell_tx",
            }
        }

        # Call the SDK sell method with the bought token amount
        sell_result = await sdk.sell(mint, bought_token_amount, user_private_key)
        print(f"Sell result: {sell_result}")

        assert sell_result["status"] is True
        assert sell_result["message"] == "Transaction completed successfully"