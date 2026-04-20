# src/wallet/pq_wallet.py
import hashlib
import time
from pqcrypto.sign.ml_dsa_44 import generate_keypair, sign, verify

class PQWallet:
    def __init__(self):
        self.public_key = None
        self.secret_key = None
        self.keygen_time = None  # opsiyonel: anahtar üretim süresini kaydet

    def generate_keypair(self):
        """ML-DSA-44 (Dilithium) ile açık ve gizli anahtar üret, süreyi ölç."""
        start = time.time()
        self.public_key, self.secret_key = generate_keypair()
        self.keygen_time = time.time() - start
        return self.public_key, self.secret_key

    def sign(self, message: bytes) -> bytes:
        """Mesajı gizli anahtarla imzala, süreyi ölç."""
        if self.secret_key is None:
            raise ValueError("Önce anahtar üretilmeli!")
        start = time.time()
        signature = sign(self.secret_key, message)
        self.sign_time = time.time() - start  # opsiyonel
        return signature

    def verify(self, message: bytes, signature: bytes, public_key: bytes = None) -> bool:
        """İmzayı doğrula, süreyi ölç."""
        pk = public_key if public_key else self.public_key
        if pk is None:
            raise ValueError("Doğrulama için açık anahtar gerekli!")
        start = time.time()
        try:
            verify(pk, message, signature)  # hata fırlatmazsa başarılı
            self.verify_time = time.time() - start
            return True
        except Exception:
            self.verify_time = time.time() - start
            return False

    def get_address(self) -> str:
        """Açık anahtarın hash'inden adres oluştur (RIPEMD-160 of SHA256)."""
        sha = hashlib.sha256(self.public_key).digest()
        ripe = hashlib.new('ripemd160', sha).digest()
        return ripe.hex()