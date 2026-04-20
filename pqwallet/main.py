import time
import hashlib
from ecdsa import SigningKey, SECP256k1
from pqcrypto.sign.ml_dsa_44 import generate_keypair, sign, verify
import seedgenerator

# Mesaj
message = b"Send 1 QuantumCoin"

# ---------------------------
# 2️⃣ Classical Wallet (ECDSA) - Seed Tabanlı
# ---------------------------
# Seed'in ilk 32 byte'ını ECDSA private key olarak kullan
sk_ecdsa = SigningKey.from_string(seedgenerator.seed_bytes[:32], curve=SECP256k1)
vk_ecdsa = sk_ecdsa.verifying_key

start = time.time()
sig_ecdsa = sk_ecdsa.sign(message)
ecdsa_sign_time = time.time() - start

ecdsa_valid = vk_ecdsa.verify(sig_ecdsa, message)

# ---------------------------
# 3️⃣ Quantum Secure Wallet (Dilithium tipi)
# ---------------------------
# Not: pqcrypto doğrudan seed tabanlı key üretmez → simülasyon
public_key, secret_key = generate_keypair()

start = time.time()
sig_dilithium = sign(secret_key, message)
dilithium_sign_time = time.time() - start

dilithium_valid = verify(public_key, message, sig_dilithium)

# ---------------------------
# 4️⃣ Sonuçları Yazdır
# ---------------------------
print("\n===== Signing Results =====")
print("ECDSA sign time:", ecdsa_sign_time, "seconds, valid:", ecdsa_valid)
print("Dilithium sign time:", dilithium_sign_time, "seconds, valid:", dilithium_valid)

print("\n===== Signature Sizes =====")
print("ECDSA signature size:", len(sig_ecdsa), "bytes")
print("Dilithium signature size:", len(sig_dilithium), "bytes")