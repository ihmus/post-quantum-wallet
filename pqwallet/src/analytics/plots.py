# src/analytics/plots.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

def create_time_comparison_chart(pq_metrics, ecdsa_metrics):
    """Zaman metrikleri (saniye) için karşılaştırmalı bar grafiği"""
    fig, ax = plt.subplots(figsize=(7, 5))
    metrics = ['Keygen', 'Sign', 'Verify']
    pq_vals = [pq_metrics['keygen_time'], pq_metrics['avg_sign_time'], pq_metrics['avg_verify_time']]
    ecdsa_vals = [ecdsa_metrics['keygen_time'], ecdsa_metrics['avg_sign_time'], ecdsa_metrics['avg_verify_time']]
    
    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width/2, pq_vals, width, label='ML-DSA-44', color='skyblue')
    ax.bar(x + width/2, ecdsa_vals, width, label='ECDSA', color='lightcoral')
    ax.set_ylabel('Süre (saniye)')
    ax.set_title('Zaman Karşılaştırması (saniye)')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    fig.tight_layout()
    return FigureCanvas(fig)

def create_size_comparison_chart(pq_metrics, ecdsa_metrics):
    """Boyut metrikleri (bayt) için karşılaştırmalı bar grafiği"""
    fig, ax = plt.subplots(figsize=(7, 5))
    metrics = ['Public Key', 'Signature']
    pq_vals = [pq_metrics['pubkey_size'], pq_metrics['avg_sig_size']]
    ecdsa_vals = [ecdsa_metrics['pubkey_size'], ecdsa_metrics['avg_sig_size']]
    
    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width/2, pq_vals, width, label='ML-DSA-44', color='skyblue')
    ax.bar(x + width/2, ecdsa_vals, width, label='ECDSA', color='lightcoral')
    ax.set_ylabel('Boyut (bayt)')
    ax.set_title('Anahtar ve İmza Boyutları')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    fig.tight_layout()
    return FigureCanvas(fig)

def create_signature_size_boxplot(pq_sizes, ecdsa_sizes):
    """İmza boyutları için kutu grafiği"""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot([pq_sizes, ecdsa_sizes], labels=['ML-DSA-44', 'ECDSA'])
    ax.set_ylabel('İmza Boyutu (bayt)')
    ax.set_title('İmza Boyutları Dağılımı')
    return FigureCanvas(fig)
def create_quantum_resilience_chart():
    """Shor algoritmasına karşı teorik dayanıklılık grafiği"""
    labels = ['ML-DSA-44 (Lattice)', 'ECDSA (secp256k1)']
    resilience_scores = [100, 0]  # 100: tam dayanıklı, 0: tamamen kırılgan

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, resilience_scores, color=['#2ecc71', '#e74c3c'])

    ax.set_ylim(0, 110)
    ax.set_ylabel('Shor Direnci (Teorik)', fontsize=12)
    ax.set_title('⚛️ Shor Algoritmasına Karşı Dayanıklılık Karşılaştırması', fontsize=14)
    ax.axhline(y=100, color='#2ecc71', linestyle='--', alpha=0.3)
    ax.text(0, 105, 'Kuantum Dirençli', ha='center', fontsize=9, color='#2ecc71')
    ax.text(1, 105, 'Kuantum Kırılgan', ha='center', fontsize=9, color='#e74c3c')
    ax.text(0.5, -0.15, 
            'Yeterli büyüklükteki bir kuantum bilgisayar, Shor algoritması ile bir ECDSA \nözel anahtarını saatler içinde kırabilir (Classical: ~10^30 yıl)',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic')
    fig.tight_layout()
    return FigureCanvas(fig)