# src/gui/comparison_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from src.analytics.benchmarks import measure_wallet_ops
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet

class ComparisonTab(QWidget):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_refresh = QPushButton("Metrikleri Yenile (Performans Testi)")
        self.btn_refresh.clicked.connect(self.refresh_metrics)
        self.table = QTableWidget(0, 3)  # satır sonradan eklenecek
        self.table.setHorizontalHeaderLabels(["Metrik", "ML-DSA-44 (PQ)", "ECDSA"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
    def refresh_metrics(self):
        self.btn_refresh.setEnabled(False)
        try:
            pq_metrics = measure_wallet_ops(PQWallet, num_iterations=5)  # hızlı test
            ecdsa_metrics = measure_wallet_ops(ECDSAWallet, num_iterations=5)
            self.populate_table(pq_metrics, ecdsa_metrics)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Metrik toplanamadı: {e}")
        finally:
            self.btn_refresh.setEnabled(True)
    
    def populate_table(self, pq, ecdsa):
        metrics = [
            ("Anahtar Üretim Süresi (s)", f"{pq['keygen_time']:.6f}", f"{ecdsa['keygen_time']:.6f}"),
            ("Açık Anahtar Boyutu (byte)", f"{pq['pubkey_size']}", f"{ecdsa['pubkey_size']}"),
            ("Ort. İmzalama Süresi (s)", f"{pq['avg_sign_time']:.6f}", f"{ecdsa['avg_sign_time']:.6f}"),
            ("Ort. İmza Boyutu (byte)", f"{pq['avg_sig_size']:.1f}", f"{ecdsa['avg_sig_size']:.1f}"),
            ("Ort. Doğrulama Süresi (s)", f"{pq['avg_verify_time']:.6f}", f"{ecdsa['avg_verify_time']:.6f}"),
        ]
        self.table.setRowCount(len(metrics))
        for i, (name, pq_val, ecdsa_val) in enumerate(metrics):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(pq_val))
            self.table.setItem(i, 2, QTableWidgetItem(ecdsa_val))
        self.table.resizeRowsToContents()