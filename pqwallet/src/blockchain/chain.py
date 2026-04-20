# src/blockchain/chain.py
from .models import Block

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", [])
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            return True
        return False

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("Madencilik yapılacak işlem yok.")
            return None
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.last_block.hash,
            transactions=self.pending_transactions
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                print(f"Blok {i} hash'i geçersiz!")
                return False
            if current.previous_hash != previous.hash:
                print(f"Blok {i} önceki hash uyuşmazlığı!")
                return False
            for tx in current.transactions:
                if not tx.is_valid():
                    print(f"Blok {i} içinde geçersiz işlem!")
                    return False
        return True