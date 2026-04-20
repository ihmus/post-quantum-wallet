# src/comparison.py
import time
import statistics
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet
from src.blockchain.models import Transaction
from src.blockchain.chain import Blockchain

def measure_wallet_ops(wallet_class, wallet_type, num_tx=5):
    """Cüzdan temel operasyonlarını ölç: anahtar üretimi, adres, imzalama, doğrulama."""
    print(f"\n--- {wallet_type} Wallet Ölçümleri ---")
    
    # 1. Anahtar üretimi
    wallet = wallet_class()
    pub, priv = wallet.generate_keypair()
    print(f"Anahtar üretim süresi: {wallet.keygen_time:.6f} s")
    print(f"Public key boyutu: {len(pub)} bayt")
    print(f"Adres: {wallet.get_address()}")
    
    # 2. İmzalama ve doğrulama süreleri (num_tx adet işlem için)
    message = b"Transfer 10 coin to Bob"
    sign_times = []
    sig_sizes = []
    verify_times = []
    
    for i in range(num_tx):
        # İmzalama
        start = time.time()
        sig = wallet.sign(message)
        sign_times.append(time.time() - start)
        sig_sizes.append(len(sig))
        
        # Doğrulama (kendi public key'i ile)
        start = time.time()
        valid = wallet.verify(message, sig)
        verify_times.append(time.time() - start)
    
    print(f"Ortalama imzalama süresi: {statistics.mean(sign_times):.6f} s")
    print(f"Ortalama imza boyutu: {statistics.mean(sig_sizes):.2f} bayt")
    print(f"Ortalama doğrulama süresi: {statistics.mean(verify_times):.6f} s")
    
    return wallet

def test_blockchain_ops(wallet_class, wallet_type):
    """Blockchain üzerinde işlem yapma sürelerini ölç."""
    print(f"\n--- {wallet_type} Blockchain Testi ---")
    
    # Cüzdanlar
    alice = wallet_class()
    alice.generate_keypair()
    bob = wallet_class()
    bob.generate_keypair()
    
    print(f"Alice adresi: {alice.get_address()}")
    print(f"Bob adresi: {bob.get_address()}")
    
    # Blockchain oluştur
    chain = Blockchain(difficulty=2)
    
    # İşlem oluşturma ve imzalama süresi
    start = time.time()
    tx = Transaction(sender=alice.get_address(), recipient=bob.get_address(), amount=10, wallet=alice, wallet_type=wallet_type)
    tx.sign(alice)
    tx_creation_time = time.time() - start
    print(f"İşlem oluşturma + imzalama süresi: {tx_creation_time:.6f} s")
    
    # İşlem doğrulama süresi
    start = time.time()
    is_valid = tx.is_valid()
    tx_validation_time = time.time() - start
    print(f"İşlem doğrulama süresi: {tx_validation_time:.6f} s")
    print(f"İşlem geçerli mi? {is_valid}")
    
    # Havuza ekle
    if chain.add_transaction(tx):
        print("İşlem havuza eklendi.")
    else:
        print("İşlem geçersiz, havuz eklenemedi!")
        return
    
    # Blok madenciliği süresi
    start = time.time()
    chain.mine_pending_transactions()
    mine_time = time.time() - start
    print(f"Blok madenciliği süresi: {mine_time:.6f} s")
    
    # Zincir geçerliliği
    print("Zincir geçerli mi?", chain.is_chain_valid())
    
    # Bloktaki işlem sayısı
    last_block = chain.last_block
    print(f"Bloktaki işlem sayısı: {len(last_block.transactions)}")
    
    return chain

def full_comparison():
    # Post-Quantum
    pq_wallet = measure_wallet_ops(PQWallet, "ML-DSA-44")
    pq_chain = test_blockchain_ops(PQWallet, "pq")
    
    # ECDSA
    ecdsa_wallet = measure_wallet_ops(ECDSAWallet, "ECDSA (secp256k1)")
    ecdsa_chain = test_blockchain_ops(ECDSAWallet, "ecdsa")

if __name__ == "__main__":
    full_comparison()