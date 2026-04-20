# src/main.py
import time
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet
from src.blockchain.models import Transaction
from src.blockchain.chain import Blockchain

def test_blockchain(wallet_class, wallet_type):
    print(f"\n🔷 {wallet_type.upper()} CÜZDAN İLE BLOCKCHAIN TESTİ")
    print("-" * 50)
    
    # 1. Cüzdanları oluştur
    alice = wallet_class()
    alice.generate_keypair()
    bob = wallet_class()
    bob.generate_keypair()
    
    print(f"👤 Alice adresi: {alice.get_address()}")
    print(f"👤 Bob adresi   : {bob.get_address()}")
    print(f"🔑 Alice public key boyutu: {len(alice.public_key)} bayt")
    
    # 2. Blockchain oluştur
    chain = Blockchain(difficulty=2)
    
    # 3. İşlem oluştur, imzala ve süreyi ölç
    tx = Transaction(sender=alice.get_address(), 
                     recipient=bob.get_address(), 
                     amount=10, 
                     wallet=alice, 
                     wallet_type=wallet_type)
    
    start = time.time()
    tx.sign(alice)
    sign_time = time.time() - start
    print(f"✍️ İmzalama süresi: {sign_time:.6f} s")
    print(f"📦 İmza boyutu: {len(tx.signature)} bayt")
    
    # 4. İşlem doğrulama süresi
    start = time.time()
    is_valid = tx.is_valid()
    verify_time = time.time() - start
    print(f"✅ İşlem doğrulama süresi: {verify_time:.6f} s")
    print(f"🔍 İşlem geçerli mi? {is_valid}")
    
    if not is_valid:
        print("❌ İşlem geçersiz, zincire eklenemiyor!")
        return
    
    # 5. Havuza ekle
    if chain.add_transaction(tx):
        print("📥 İşlem havuza eklendi.")
    
    # 6. Madencilik süresi
    start = time.time()
    chain.mine_pending_transactions()
    mine_time = time.time() - start
    print(f"⛏️ Blok madenciliği süresi: {mine_time:.6f} s")
    
    # 7. Zincir geçerliliği
    print(f"🔗 Zincir geçerli mi? {chain.is_chain_valid()}")
    
    # 8. Blok bilgisi
    last_block = chain.last_block
    print(f"📊 Son blok: #{last_block.index} | Hash: {last_block.hash[:16]}...")
    print(f"📊 Bloktaki işlem sayısı: {len(last_block.transactions)}")
    
    return chain

def main():
    print("🚀 POST-QUANTUM BLOCKCHAIN SİMÜLATÖRÜ")
    print("======================================")
    
    # Post‑Quantum testi
    pq_chain = test_blockchain(PQWallet, "pq")
    
    # ECDSA testi
    ecdsa_chain = test_blockchain(ECDSAWallet, "ecdsa")
    
    print("\n📈 KARŞILAŞTIRMA ÖZETİ")
    print("======================")
    # Basit özet (isterseniz daha detaylı ekleyebilirsiniz)
    print("• ML-DSA-44 (Post‑Quantum) vs ECDSA (secp256k1)")
    print("• İmza boyutları: Yukarıdaki çıktılara bakınız.")
    print("• Süreler: Yukarıdaki çıktılarda görülmektedir.")
    print("\n✅ Tüm testler tamamlandı.")

if __name__ == "__main__":
    main()