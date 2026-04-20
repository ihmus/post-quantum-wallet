# src/wallet/ecdsa_wallet.py
import hashlib
import time
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class ECDSAWallet:
    def __init__(self):
        self.private_key = None  # SigningKey nesnesi
        self.public_key = None   # bytes olarak saklanacak
        self.keygen_time = None

    def generate_keypair(self):
        start = time.time()
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.get_verifying_key()
        self.private_key = sk
        self.public_key = vk.to_string()  # bytes
        self.keygen_time = time.time() - start
        return self.public_key, self.private_key.to_string()

    def sign(self, message: bytes) -> bytes:
        if self.private_key is None:
            raise ValueError("Önce anahtar üretilmeli!")
        start = time.time()
        signature = self.private_key.sign(message)
        self.sign_time = time.time() - start
        return signature

    def verify(self, message: bytes, signature: bytes, public_key: bytes = None) -> bool:
        if public_key is None:
            pk_bytes = self.public_key
        else:
            pk_bytes = public_key
        vk = VerifyingKey.from_string(pk_bytes, curve=SECP256k1)
        start = time.time()
        try:
            result = vk.verify(signature, message)
            self.verify_time = time.time() - start
            return result
        except Exception:
            self.verify_time = time.time() - start
            return False

    def get_address(self) -> str:
        """Açık anahtarın hash'inden adres (RIPEMD-160 of SHA256)"""
        sha = hashlib.sha256(self.public_key).digest()
        ripe = hashlib.new('ripemd160', sha).digest()
        return ripe.hex()