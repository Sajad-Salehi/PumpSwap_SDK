
### Using Poetry

```bash
poetry add pumpswap-sdk
```

### Using pip

```bash
pip install pumpswap-sdk
```

### Usage

Here’s how to get started with the PumpSwap SDK in your Python project.

1. **Initialize the SDK**

```python
from pumpswap import PumpSwapSDK
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
