# src/analytics/benchmarks.py
import time
import statistics
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet

def measure_wallet_ops(wallet_class, num_iterations=10):
    """
    wallet_class: PQWallet veya ECDSAWallet
    num_iterations: İmzalama/doğrulama için tekrar sayısı
    Returns: dict with metrics
    """
    wallet = wallet_class()
    
    # Anahtar üretim süresi
    start = time.time()
    pub, priv = wallet.generate_keypair()
    keygen_time = time.time() - start
    
    pubkey_size = len(pub)
    
    # Test mesajı
    message = b"Benchmark message for post-quantum blockchain"
    
    sign_times = []
    sig_sizes = []
    verify_times = []
    
    for _ in range(num_iterations):
        # İmzalama
        start = time.time()
        sig = wallet.sign(message)
        sign_times.append(time.time() - start)
        sig_sizes.append(len(sig))
        
        # Doğrulama
        start = time.time()
        valid = wallet.verify(message, sig)
        verify_times.append(time.time() - start)
        if not valid:
            raise ValueError("Doğrulama başarısız!")
    
    return {
        'keygen_time': keygen_time,
        'pubkey_size': pubkey_size,
        'avg_sign_time': statistics.mean(sign_times),
        'std_sign_time': statistics.stdev(sign_times) if len(sign_times) > 1 else 0,
        'avg_sig_size': statistics.mean(sig_sizes),
        'std_sig_size': statistics.stdev(sig_sizes) if len(sig_sizes) > 1 else 0,
        'avg_verify_time': statistics.mean(verify_times),
        'std_verify_time': statistics.stdev(verify_times) if len(verify_times) > 1 else 0,
    }

def measure_blockchain_ops(blockchain, wallet, num_tx=5):
    """
    Blok zinciri üzerinde işlem ekleme ve madencilik sürelerini ölçer.
    """
    # Bu fonksiyonu daha sonra genişletebiliriz
    pass