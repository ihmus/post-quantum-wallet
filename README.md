# Post-Quantum Wallet / Blockchain Simulator

Post-Quantum Wallet, ML-DSA-44 (Dilithium) tabanlı kuantum-güvenli cüzdan ile klasik ECDSA cüzdanı karşılaştıran, PyQt5 arayüzlü bir blockchain simülatörüdür. Proje; anahtar üretimi, imzalama, doğrulama, blok üretimi ve performans ölçümlerini aynı uygulama içinde sunar.

## Özellikler

- **Post-quantum imza desteği**: `pqcrypto.sign.ml_dsa_44` ile ML-DSA-44 kullanır.
- **Klasik ECDSA karşılaştırması**: `secp256k1` üzerinde çalışan ECDSA cüzdanı ile yan yana kıyaslama yapar.
- **Blockchain simülasyonu**: İşlem havuzu, genesis blok, proof-of-work ve zincir doğrulama içerir.
- **PyQt5 masaüstü arayüzü**: Cüzdan, Blockchain, Analiz ve Karşılaştırma sekmeleri.
- **Performans ölçümü**: Anahtar üretim süresi, imza boyutu, imzalama ve doğrulama sürelerini ölçer.
- **Grafik ve analiz**: Matplotlib / seaborn / pandas ile görselleştirme desteği.
- **Seed üretimi**: `seedgenerator.py` ile 12 kelimelik mnemonic seed oluşturma örneği.

## Teknoloji Yığını

- Python 3
- PyQt5
- pqcrypto
- ecdsa
- matplotlib
- seaborn
- pandas
- numpy
- mnemonic
- web3
- eth-keys
- eth-account

## Proje Yapısı

```text
pqwallet/
├── main.py
├── requirements.txt
├── seedgenerator.py
├── src
│   ├── analytics
│   │   ├── benchmarks.py
│   │   ├── __init__.py
│   │   ├── plots.py
│   │   ├── __pycache__
│   │   │   ├── benchmarks.cpython-311.pyc
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   └── plots.cpython-311.pyc
│   │   └── stats.py
│   ├── blockchain
│   │   ├── chain.py
│   │   ├── config.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── __pycache__
│   │       ├── chain.cpython-311.pyc
│   │       ├── __init__.cpython-311.pyc
│   │       └── models.cpython-311.pyc
│   ├── comparison.py
│   ├── gui
│   │   ├── analytics_tab.py
│   │   ├── blockchain_tab.py
│   │   ├── comparison_tab.py
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── __pycache__
│   │   │   ├── analytics_tab.cpython-311.pyc
│   │   │   ├── blockchain_tab.cpython-311.pyc
│   │   │   ├── comparison_tab.cpython-311.pyc
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── main_window.cpython-311.pyc
│   │   │   ├── shor_video_tab.cpython-311.pyc
│   │   │   └── wallet_tab.cpython-311.pyc
│   │   ├── shor_video_tab.py
│   │   ├── styles.py
│   │   └── wallet_tab.py
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   │   ├── comparison.cpython-311.pyc
│   │   ├── __init__.cpython-311.pyc
│   │   └── main.cpython-311.pyc
│   ├── simulation
│   │   ├── __init__.py
│   │   ├── miner.py
│   │   ├── runner.py
│   │   └── tx_generator.py
│   └── wallet
│       ├── ecdsa_wallet.py
│       ├── __init__.py
│       ├── mnemonic_utils.py
│       ├── pq_wallet.py
│       └── __pycache__
│           ├── ecdsa_wallet.cpython-311.pyc
│           ├── __init__.cpython-311.pyc
│           └── pq_wallet.cpython-311.pyc
├── data
│   └── logs
├── docs
│   ├── presentation.pptx
│   └── project_report.tex (or .md)
└── tests
    ├── test_blockchain.py
    ├── test_integration.py
    └── test_wallet.py
```

## Kurulum

Önce sanal ortam oluşturun:

```bash
python -m venv .venv
```

Sanal ortamı etkinleştirin:

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

GUI uygulamasını başlatmak için proje kök klasöründe şu komutu kullanın:

```bash
python main.py
```

CLI / test akışını çalıştırmak için:

```bash
python -m src.main
```

## Nasıl Çalışır?

### 1. Cüzdanlar
- `PQWallet`: ML-DSA-44 ile anahtar üretir, mesaj imzalar ve doğrular.
- `ECDSAWallet`: Klasik `secp256k1` tabanlı ECDSA uygulamasıdır.
- Her iki cüzdan da adres üretiminde `SHA-256 + RIPEMD-160` yaklaşımını kullanır.

### 2. İşlemler
`Transaction` nesnesi:
- gönderici,
- alıcı,
- miktar,
- wallet tipi (`pq` veya `ecdsa`),
- imza ve açık anahtar

bilgilerini taşır. İşlemin geçerliliği cüzdan tipine göre doğrulanır.

### 3. Blockchain
- Genesis blok oluşturulur.
- Geçerli işlemler bekleyen havuza eklenir.
- `mine_pending_transactions()` ile basit proof-of-work uygulanarak yeni blok üretilir.
- Zincir bütünlüğü `is_chain_valid()` ile kontrol edilir.

### 4. Arayüz
Uygulama içinde dört ana sekme bulunur:
- **Cüzdan**: Cüzdan işlemleri
- **Blockchain**: Blok ve işlem görünümü
- **Analiz**: Benchmark ve grafikler
- **Karşılaştırma**: ML-DSA-44 ve ECDSA metrikleri

## Notlar

- Proje aktif olarak bir **simülatör** olarak tasarlanmıştır; gerçek bir blokzincir ağına doğrudan bağlı değildir.
- Post-quantum imza tarafında `pqcrypto.sign.ml_dsa_44` kullanılır.
- GUI başlatıcısı `main.py` içindedir; bu yüzden uygulamayı repo kökünden çalıştırmak en güvenli yöntemdir.

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
