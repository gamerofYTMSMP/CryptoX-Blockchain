import hashlib
import time
import random
import requests
from hashlib import sha256

# Coin parameters
COIN_NAME = "CryptoX"
COIN_SYMBOL = "CX"
TOTAL_SUPPLY = 50000000  # Total coins
PRE_MINED = 25000000     # Pre-mined coins in your wallet

# Wallet (Your pre-mined coins stored here)
pre_mined_wallet = {
    "address": "CXPreMinerAddress123456789",  # Placeholder address
    "balance": PRE_MINED,
}

# Blockchain structure
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = f"{index}{previous_hash}{timestamp}{data}"
        return sha256(value.encode('utf-8')).hexdigest()

    def add_block(self, data):
        index = len(self.chain)
        previous_block = self.chain[-1]
        previous_hash = previous_block.hash
        timestamp = time.time()
        block_hash = self.calculate_hash(index, previous_hash, timestamp, data)
        new_block = Block(index, previous_hash, timestamp, data, block_hash)
        self.chain.append(new_block)

# Proof of Work Algorithm (Mining)
class ProofOfWork:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def mine_block(self, data):
        block = self.blockchain.chain[-1]
        index = len(self.blockchain.chain)
        previous_hash = block.hash
        timestamp = time.time()

        # Simple proof of work (difficulty)
        target = 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        while True:
            nonce = random.randint(0, 2**64)
            hash_value = sha256(f"{index}{previous_hash}{timestamp}{data}{nonce}".encode('utf-8')).hexdigest()
            if int(hash_value, 16) < target:
                print(f"Block mined: {data}")
                self.blockchain.add_block(data)
                break

# Dynamic difficulty adjustment (based on mining rate)
class DifficultyAdjuster:
    def __init__(self):
        self.target_block_time = 600  # 10 minutes in seconds
        self.blocks_per_difficulty_change = 2016
        self.difficulty = 1

    def adjust_difficulty(self, blockchain):
        if len(blockchain.chain) % self.blocks_per_difficulty_change == 0:
            block_times = [blockchain.chain[i + 1].timestamp - blockchain.chain[i].timestamp for i in range(len(blockchain.chain) - 1)]
            avg_time_per_block = sum(block_times) / len(block_times)
            if avg_time_per_block < self.target_block_time:
                self.difficulty += 1
            else:
                self.difficulty -= 1
            print(f"Difficulty adjusted to {self.difficulty}")

# Transaction fees and pool management
class Transaction:
    def __init__(self, sender, recipient, amount, fee=0.08):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee

    def calculate_fee(self):
        return self.amount * self.fee

# API to fetch CoinMarketCap data
class CoinMarketCapAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    
    def get_coin_data(self):
        headers = {
            'X-CMC_PRO_API_KEY': self.api_key,
            'Accept': 'application/json',
        }
        response = requests.get(self.url, headers=headers)
        return response.json()

# Main Application Logic
if __name__ == "__main__":
    # Initialize blockchain and miner
    blockchain = Blockchain()
    miner = ProofOfWork(blockchain)
    difficulty_adjuster = DifficultyAdjuster()
    coinmarketcap_api = CoinMarketCapAPI("228ec0fa-e903-4056-82c2-421e431712ac")

    # CoinMarketCap API fetch (example usage)
    coin_data = coinmarketcap_api.get_coin_data()
    print(f"CoinMarketCap Data: {coin_data}")
    
    # Start mining process
    miner.mine_block("Block data for CryptoX Coin")
    
    # Adjust mining difficulty if needed
    difficulty_adjuster.adjust_difficulty(blockchain)
    
    # Example transaction
    transaction = Transaction("CXPreMinerAddress123456789", "CXUserAddress987654321", 10)
    fee = transaction.calculate_fee()
    print(f"Transaction fee: {fee} CX")

