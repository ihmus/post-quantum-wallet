# src/analytics/plots.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

def create_comparison_bar_chart(pq_metrics, ecdsa_metrics):
    """
    İki algoritmanın karşılaştırmalı bar grafiği.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    
    metrics = ['Keygen Time (s)', 'Sign Time (s)', 'Verify Time (s)', 'Sig Size (bytes)', 'Pubkey Size (bytes)']
    pq_values = [
        pq_metrics['keygen_time'],
        pq_metrics['avg_sign_time'],
        pq_metrics['avg_verify_time'],
        pq_metrics['avg_sig_size'],
        pq_metrics['pubkey_size']
    ]
    ecdsa_values = [
        ecdsa_metrics['keygen_time'],
        ecdsa_metrics['avg_sign_time'],
        ecdsa_metrics['avg_verify_time'],
        ecdsa_metrics['avg_sig_size'],
        ecdsa_metrics['pubkey_size']
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax.bar(x - width/2, pq_values, width, label='ML-DSA-44 (PQ)', color='skyblue')
    ax.bar(x + width/2, ecdsa_values, width, label='ECDSA (secp256k1)', color='lightcoral')
    
    ax.set_ylabel('Değerler')
    ax.set_title('Post-Quantum vs Classical Performans Karşılaştırması')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=45, ha='right')
    ax.legend()
    
    fig.tight_layout()
    return FigureCanvas(fig)

def create_signature_size_comparison(pq_sizes, ecdsa_sizes):
    """İmza boyutları için kutu grafiği (boxplot) veya histogram"""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([pq_sizes, ecdsa_sizes], labels=['ML-DSA-44', 'ECDSA'])
    ax.set_ylabel('İmza Boyutu (bayt)')
    ax.set_title('İmza Boyutları Dağılımı')
    return FigureCanvas(fig)