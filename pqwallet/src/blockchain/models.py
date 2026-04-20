# src/blockchain/models.py
import json
import hashlib
import time

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, wallet=None, wallet_type="pq"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.wallet_type = wallet_type
        self.signature = None
        self.public_key = wallet.public_key if wallet else None

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "wallet_type": self.wallet_type,
            "public_key": self.public_key.hex() if self.public_key else None
        }

    def hash(self):
        tx_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(tx_data).digest()

    def sign(self, wallet):
        if wallet.public_key != self.public_key:
            raise ValueError("Cüzdan bu işleme ait değil!")
        tx_hash = self.hash()
        self.signature = wallet.sign(tx_hash)

    def is_valid(self) -> bool:
        if not self.signature or not self.public_key:
            return False
        # Adres kontrolü
        sha = hashlib.sha256(self.public_key).digest()
        ripe = hashlib.new('ripemd160', sha).digest()
        if ripe.hex() != self.sender:
            return False
        tx_hash = self.hash()
        # Wallet tipine göre doğrulayıcı oluştur
        if self.wallet_type == "pq":
            from src.wallet.pq_wallet import PQWallet
            verifier = PQWallet()
        elif self.wallet_type == "ecdsa":
            from src.wallet.ecdsa_wallet import ECDSAWallet
            verifier = ECDSAWallet()
        else:
            raise ValueError("Bilinmeyen wallet tipi")
        verifier.public_key = self.public_key
        return verifier.verify(tx_hash, self.signature)


class Block:
    def __init__(self, index, previous_hash, transactions, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
        print(f"Blok {self.index} madenciliği tamamlandı: {self.hash}")