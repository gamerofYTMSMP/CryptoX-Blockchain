import hashlib
import time
import random
from collections import deque

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = deque()
        self.create_genesis_block()

        # Pre-mine 25M coins to the owner's address (you can change this address)
        self.owner_wallet = "YourWalletAddressHere"
        self.total_supply = 50000000  # Total supply of coins
        self.mined_supply = 0
        self.owner_balance = 25000000  # Pre-mine the 25M to your wallet

    def create_genesis_block(self):
        """Generate the first block in the chain"""
        genesis_block = Block(index=0, previous_hash="0", timestamp=time.time(), transactions=[], nonce=0)
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def add_block(self, block):
        """Add a new block to the blockchain"""
        self.chain.append(block)

    def mine_block(self, miner_wallet):
        """Proof of Work and Proof of Stake mining combined"""

        # Proof of Work mining (SHA-256 with difficulty)
        difficulty = self.get_difficulty()
        nonce = 0
        last_block = self.chain[-1]
        while True:
            block_data = f"{last_block.hash}{str(nonce)}"
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()

            if block_hash[:difficulty] == '0' * difficulty:
                break
            nonce += 1

        # Create a new block with the proof
        block = Block(index=len(self.chain), previous_hash=last_block.hash, timestamp=time.time(),
                      transactions=self.pending_transactions, nonce=nonce)
        block.hash = block.calculate_hash()
        
        # Add block to chain
        self.add_block(block)

        # Reward miner based on PoW (Proof of Work) and PoS (Proof of Stake)
        self.reward_miner(miner_wallet, block)

        # Clear the pending transactions
        self.pending_transactions.clear()
        print(f"Block mined by {miner_wallet} with hash: {block.hash}")

    def reward_miner(self, miner_wallet, block):
        """Reward the miner with a fixed amount of coins"""
        reward = 8.5  # Coins per block mined
        transaction = {
            "sender": "network",
            "receiver": miner_wallet,
            "amount": reward
        }
        self.pending_transactions.append(transaction)
        self.mined_supply += reward

    def get_difficulty(self):
        """Adjust difficulty based on the block generation speed (like Bitcoin)"""
        target_block_time = 10  # Target block time in minutes
        time_per_block = (time.time() - self.chain[-1].timestamp) / 60  # Time per block in minutes
        if time_per_block < target_block_time:
            difficulty = min(5, len(self.chain) // 10)  # Increase difficulty as mining speed increases
        else:
            difficulty = max(1, len(self.chain) // 20)  # Decrease difficulty if mining slows down
        return difficulty

    def create_transaction(self, sender_wallet, receiver_wallet, amount):
        """Create a new transaction"""
        if self.mined_supply + amount > self.total_supply:
            print("Not enough coins available!")
            return

        transaction = {
            "sender": sender_wallet,
            "receiver": receiver_wallet,
            "amount": amount
        }
        self.pending_transactions.append(transaction)
        print(f"Transaction created: {sender_wallet} -> {receiver_wallet} for {amount} coins")

    def print_chain(self):
        """Print the entire blockchain"""
        for block in self.chain:
            print(f"Block {block.index} - Hash: {block.hash} - Transactions: {block.transactions}")

# Block class
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = ''

    def calculate_hash(self):
        """Calculate the hash of the block"""
        block_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()


# Main function to simulate the blockchain operations
if __name__ == "__main__":
    blockchain = Blockchain()

    # Example: Miner tries to mine a block
    miner_wallet = "MinerWalletAddressHere"
    blockchain.mine_block(miner_wallet)

    # Example: Create a transaction
    blockchain.create_transaction("User1", "User2", 50)

    # Print the blockchain
    blockchain.print_chain()
