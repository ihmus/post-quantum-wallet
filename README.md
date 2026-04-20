# Post-Quantum Blockchain Simülatörü – Proje Özeti

## ✅ Tamamlanan Aşamalar

### Aşama 1 – Core Wallet Modülü

- Post‑quantum cüzdan (`src/wallet/pq_wallet.py`): ML-DSA-44 (Dilithium) kullanır.
  - `generate_keypair`, `sign`, `verify`, `get_address` metodları.
  - Anahtar üretimi, imzalama ve doğrulama süreleri ölçülür.
  - Adres: SHA256 + RIPEMD‑160 (hex).
- Klasik ECDSA cüzdan (`src/wallet/ecdsa_wallet.py`): secp256k1 eğrisi.
  - Aynı arayüz, public key bytes olarak saklanır.
  - `VerifyingKey.from_string` ile doğrulama.

### Aşama 2 – Blockchain Engine

- `src/blockchain/models.py`: `Transaction`, `Block` sınıfları.
  - `Transaction` içinde `wallet_type` alanı (`"pq"` veya `"ecdsa"`) ile hangi wallet tipinin kullanıldığı belirtilir.
  - `is_valid()` metodu, `wallet_type`'a göre doğru wallet sınıfını dinamik olarak import eder.
- `src/blockchain/chain.py`: `Blockchain` sınıfı.
  - Zincir yönetimi, bekleyen işlemler havuzu, proof‑of‑work (basit nonce), zincir doğrulama.
- `src/blockchain/config.py`: `DIFFICULTY` sabiti.

### Aşama 3 – Simülasyon & Karşılaştırma (Kısmen)

- `src/comparison.py`: Her iki wallet için kriptografik operasyonları ve blockchain işlemlerini ölçer.
  - Anahtar üretim süresi, public key boyutu, imzalama süresi, imza boyutu, doğrulama süresi.
  - Alice → Bob işlem oluşturma, imzalama, doğrulama, blok madenciliği süreleri.
- `src/main.py`: Her iki wallet ile blockchain testini çalıştırır, adresleri ve süreleri ekrana basar.

## 🚧 Sıradaki Aşamalar

### Aşama 4 – PyQt5 GUI

- Klasör: `src/gui/`
  - `main_window.py`: Ana pencere (tab’lar: Wallet, Blockchain, Analytics).
  - `wallet_tab.py`: Cüzdan oluşturma, adres görüntüleme, işlem gönderme.
  - `blockchain_tab.py`: Blok listesi, işlem detayları.
  - `analytics_tab.py`: Grafikler (matplotlib FigureCanvas).
- PyQt5 ile backend bağlantısı: wallet ve blockchain nesneleri GUI’den kontrol edilir.

### Aşama 5 – Analytics Modülü

- `src/analytics/` klasörü.
  - `benchmarks.py`: Toplu ölçümler (çok sayıda işlem, farklı mesaj boyutları).
  - `plots.py`: Karşılaştırmalı grafikler (imza boyutu, süreler) – seaborn/matplotlib.
  - `stats.py`: Zincir istatistikleri (blok süreleri, işlem sayısı).

### Aşama 6 – Dokümantasyon & Sunum

- `README.md` güncellenecek.
- Proje raporu (PDF/Word) ve sunum hazırlığı.


## Güncel Dosya Yapısı
```plaintext
src/
├── __init__.py
├── main.py
├── comparison.py
├── wallet/
│   ├── __init__.py
│   ├── pq_wallet.py
│   └── ecdsa_wallet.py
├── blockchain/
│   ├── __init__.py
│   ├── models.py
│   ├── chain.py
│   └── config.py
├── gui/               # (ileride)
└── analytics/         # (ileride) 
```
## 🔧 Dosya mimarisi
```
post_quantum_blockchain/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # Entry point: launches GUI or CLI
│   │
│   ├── wallet/
│   │   ├── __init__.py
│   │   ├── pq_wallet.py             # Post‑quantum wallet implementation
│   │   ├── ecdsa_wallet.py           # Classical wallet for comparison
│   │   └── mnemonic_utils.py         # BIP39 mnemonic to seed
│   │
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── models.py                 # Block, Transaction classes
│   │   ├── chain.py                  # Blockchain class and validation
│   │   └── config.py                 # e.g., DIFFICULTY, BLOCK_TIME
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py             # PyQt5 main window
│   │   ├── wallet_tab.py              # Wallet UI
│   │   ├── blockchain_tab.py          # Blockchain viewer
│   │   ├── analytics_tab.py           # Plotting UI
│   │   └── styles.py                  # QSS stylesheets
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── benchmarks.py              # Keygen/sign/verify timing
│   │   ├── plots.py                   # Matplotlib plotting functions
│   │   └── stats.py                   # Blockchain statistics
│   │
│   └── simulation/
│       ├── __init__.py
│       ├── tx_generator.py             # Generate random transactions
│       ├── miner.py                    # Simple mining simulation
│       └── runner.py                    # Run test scenarios
│
├── tests/
│   ├── test_wallet.py
│   ├── test_blockchain.py
│   └── test_integration.py
│
├── data/
│   └── logs
│
└── docs/
    ├── project_report.tex (or .md)
    └── presentation.pptx
```
    
## 🔧 Kritik Kod Parçacıkları (Özet)

1. **ECDSA Wallet (public key bytes olarak)**
```python
self.public_key = vk.to_string()  # bytes
# verify içinde:
vk = VerifyingKey.from_string(pk_bytes, curve=SECP256k1)
vk.verify(signature, message)
