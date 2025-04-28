import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.transaction import Transaction  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solana.transaction import Message
from solana.rpc.types import TxOpts
from solders.instruction import Instruction # type: ignore


# This function confirms a transaction on the Solana blockchain.
async def confirm_transaction(client: AsyncClient, tx_signature, max_retries: int = 5, delay: float = 1) -> bool:
    for attempt in range(max_retries):
        try:
            res = await client.confirm_transaction(tx_signature, commitment=Confirmed)
            if res:
                return res
            else:
                continue
            
        except Exception as e:
            print(f"Error confirming transaction (attempt {attempt + 1}): {e}")
        
        await asyncio.sleep(delay)

    print("Transaction confirmation failed after max retries.")
    return False



# This function sends a transaction to the Solana blockchain. 
async def send_transaction(client: AsyncClient, payer: Keypair, signers: list[Keypair], instructions: list[Instruction], commitment="confirmed") -> str | None:
    try:
        message = Message(instructions, payer.pubkey())
        latest_blockhash = (await client.get_latest_blockhash()).value.blockhash

        # Create the transaction
        transaction = Transaction(signers, message, latest_blockhash)

        # Send the transaction
        tx_signature = await client.send_transaction(
            transaction,
            opts=TxOpts(
                skip_preflight=False, 
                preflight_commitment=commitment
            ),
        )

        return tx_signature

    except Exception as e:
        print(f"Transaction failed: {e}")
        return None