# src/gui/analytics_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox, QTabWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from src.analytics.benchmarks import measure_wallet_ops
from src.analytics.plots import (
    create_time_comparison_chart,
    create_size_comparison_chart,
    create_signature_size_boxplot,
    create_quantum_resilience_chart
)
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet

class BenchmarkThread(QThread):
    finished = pyqtSignal(dict, dict, list, list)
    error = pyqtSignal(str)
    
    def __init__(self, num_iterations=10):
        super().__init__()
        self.num_iterations = num_iterations
        
    def run(self):
        try:
            pq_metrics = measure_wallet_ops(PQWallet, self.num_iterations)
            ecdsa_metrics = measure_wallet_ops(ECDSAWallet, self.num_iterations)
            
            # İmza boyutu listelerini topla
            pq_sizes = []
            ecdsa_sizes = []
            pq_w = PQWallet()
            pq_w.generate_keypair()
            ec_w = ECDSAWallet()
            ec_w.generate_keypair()
            msg = b"Benchmark"
            for _ in range(self.num_iterations):
                pq_sizes.append(len(pq_w.sign(msg)))
                ecdsa_sizes.append(len(ec_w.sign(msg)))
            
            self.finished.emit(pq_metrics, ecdsa_metrics, pq_sizes, ecdsa_sizes)
        except Exception as e:
            self.error.emit(str(e))

class AnalyticsTab(QWidget):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_run = QPushButton("Performans Testi Başlat")
        self.btn_run.clicked.connect(self.run_benchmark)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.canvas_placeholder = QLabel("Testi başlatmak için butona tıklayın.")
        self.canvas_placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addWidget(self.canvas_placeholder)
        self.setLayout(layout)
        
    def run_benchmark(self):
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.thread = BenchmarkThread(num_iterations=10)
        self.thread.finished.connect(self.on_benchmark_finished)
        self.thread.error.connect(self.on_benchmark_error)
        self.thread.start()
        
    def on_benchmark_finished(self, pq_metrics, ecdsa_metrics, pq_sizes, ecdsa_sizes):
        self.progress.setVisible(False)
        self.btn_run.setEnabled(True)
        
        # Grafikleri oluştur
        time_canvas = create_time_comparison_chart(pq_metrics, ecdsa_metrics)
        size_canvas = create_size_comparison_chart(pq_metrics, ecdsa_metrics)
        box_canvas = create_signature_size_boxplot(pq_sizes, ecdsa_sizes)
        resilience_canvas = create_quantum_resilience_chart()
        
        # Sekmeli görünüm
        tabs = QTabWidget()
        tabs.addTab(time_canvas, "Zaman Karşılaştırması")
        tabs.addTab(size_canvas, "Boyut Karşılaştırması")
        tabs.addTab(box_canvas, "İmza Boyutu Dağılımı")
        tabs.addTab(resilience_canvas, "⚛️ Kuantum Direnci")
        
        # Eski placeholder'ı değiştir
        layout = self.layout()
        layout.replaceWidget(self.canvas_placeholder, tabs)
        self.canvas_placeholder.deleteLater()
        self.canvas_placeholder = tabs
        
        # Detaylı metrik mesajı
        msg = (f"ML-DSA-44:\n"
               f"  Keygen: {pq_metrics['keygen_time']:.6f} s\n"
               f"  Sign: {pq_metrics['avg_sign_time']:.6f} s\n"
               f"  Verify: {pq_metrics['avg_verify_time']:.6f} s\n"
               f"  Sig size: {pq_metrics['avg_sig_size']:.1f} bytes\n"
               f"  Pubkey size: {pq_metrics['pubkey_size']} bytes\n\n"
               f"ECDSA:\n"
               f"  Keygen: {ecdsa_metrics['keygen_time']:.6f} s\n"
               f"  Sign: {ecdsa_metrics['avg_sign_time']:.6f} s\n"
               f"  Verify: {ecdsa_metrics['avg_verify_time']:.6f} s\n"
               f"  Sig size: {ecdsa_metrics['avg_sig_size']:.1f} bytes\n"
               f"  Pubkey size: {ecdsa_metrics['pubkey_size']} bytes")
        QMessageBox.information(self, "Ölçüm Sonuçları", msg)
        
    def on_benchmark_error(self, err_msg):
        self.progress.setVisible(False)
        self.btn_run.setEnabled(True)
        QMessageBox.critical(self, "Hata", f"Ölçüm sırasında hata: {err_msg}")