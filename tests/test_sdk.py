import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, AsyncMock
from pumpswap import PumpSwapSDK


mint = "your-token-mint-address"  # Replace with a valid mint address on pumpswap
user_private_key = "your-private-key"  # Replace with a valid private key
token_amount = 10.0 # Example token amount to sell
sol_amount = 0.0001 # Example SOL amount to buy


@pytest.mark.asyncio
async def test_buy():
    sdk = PumpSwapSDK()

    # Mock the buy_pumpswap_token function
    with patch('pumpswap.core.buy_service.buy_pumpswap_token', new_callable=AsyncMock) as mock_buy:
        mock_buy.return_value = "buy_success"

        # Call the SDK method
        result = await sdk.buy(mint, sol_amount, user_private_key)

        # Assert the result and the function call
        assert result["status"] is True
        assert result["message"] == "Transaction completed successfully"


@pytest.mark.asyncio
async def test_sell():
    sdk = PumpSwapSDK()

    # Mock the sell_pumpswap_token function
    with patch('pumpswap.core.sell_service.sell_pumpswap_token', new_callable=AsyncMock) as mock_sell:
        mock_sell.return_value = "sell_success"

        # Call the SDK method
        result = await sdk.sell(mint, token_amount, user_private_key)

        # Assert the result and the function call
        assert result["status"] is True
        assert result["message"] == "Transaction completed successfully"
