# PumpSwap SDK

A Python SDK for interacting with the PumpSwap decentralized exchange (DEX) on the Solana blockchain. This SDK simplifies buying, selling, token price retrieval, and pool data access on the PumpSwap platform, allowing developers to integrate Solana-based trading into their applications with ease.

## Features

- **Buy and Sell Tokens**: Easily interact with PumpSwap’s liquidity pools to buy and sell tokens.
- **Pool Analytics**: Detailed liquidity pool statistics
- **Price Retrieval**: Fetch the current price of a token in the market.
- **Transaction Handling**: Handle transactions securely with support for signing and sending transactions.
- **Solana Blockchain Integration**: Built specifically for Solana, leveraging libraries like `solana` and `solders`.

## Installation

You can install the PumpSwap SDK using [Poetry](https://python-poetry.org/) or `pip`.

### Using Poetry

```bash
poetry add pumpswap-sdk
```

### Using pip

```bash
pip install pumpswap-sdk
```


---

## Setup

Before using the SDK, create a `.env` file in your project root with the following environment variables:

```bash
HTTPS_RPC_ENDPOINT=your_rpc_url_here
BUY_SLIPPAGE=0.3
SELL_SLIPPAGE=0.1
SWAP_PRIORITY_FEE=1500000
```

Example `.env`:

```bash
HTTPS_RPC_ENDPOINT=https://api.mainnet-beta.solana.com
BUY_SLIPPAGE=0.3
SELL_SLIPPAGE=0.1
SWAP_PRIORITY_FEE=1500000
```

---

### Usage

Here’s how to get started with the PumpSwap SDK in your Python project.

1. **Initialize the SDK**

```python
from pumpswap_sdk import PumpSwapSDK
from solders.pubkey import Pubkey

# Initialize the SDK
sdk = PumpSwapSDK()

# Example data
mint = "EiKZAWphC65hFKz9kygWgKGcRZUGgdMmH2zSPtbGpump"
user_private_key = "your_private_key_here"
quote_account_pubkey = Pubkey.from_string("quote_account_public_key")
```

2. **Buy Tokens**

```python
# Buy tokens
sol_amount = 0.0001  # Amount of SOL you want to spend
result = await sdk.buy(mint, sol_amount, user_private_key)

print(result)
```

3. **Sell Tokens**

```python
# Sell tokens
token_amount = 10.0  # Amount of tokens you want to sell
result = await sdk.sell(mint, token_amount, user_private_key)

print(result)
```

4. **Get Token Price**

```python
# Get the price of a token
token_price = await sdk.get_token_price(mint)

print(f"Token Price: {token_price}")
```

### Development

If you want to contribute to the SDK or run tests locally, follow these steps:

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/pumpswap-sdk.git
cd pumpswap-sdk
```

2. **Install dependencies:**

```bash
poetry install
```

3. **Run tests:**

To run tests with `pytest`, use the following command:

```bash
poetry run pytest
```

4. **Build the package:**

To build the SDK package locally:

```bash
poetry build
```

### License

This project is licensed under the MIT License - see the LICENSE file for details.



### Contact

For more information, or if you have any questions, feel free to contact the author:
- **Email**: SajadSolidity@gmail.com

