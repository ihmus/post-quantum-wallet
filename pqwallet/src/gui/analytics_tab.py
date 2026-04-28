# src/gui/analytics_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from src.analytics.benchmarks import measure_wallet_ops
from src.analytics.plots import create_comparison_bar_chart, create_signature_size_comparison
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet
from PyQt5.QtCore import Qt 

class BenchmarkThread(QThread):
    finished = pyqtSignal(dict, dict, list, list)  # pq_metrics, ecdsa_metrics, pq_sizes, ecdsa_sizes
    error = pyqtSignal(str)
    
    def __init__(self, num_iterations=10):
        super().__init__()
        self.num_iterations = num_iterations
        
    def run(self):
        try:
            # PQ ölçümü
            pq_metrics = measure_wallet_ops(PQWallet, self.num_iterations)
            # ECDSA ölçümü
            ecdsa_metrics = measure_wallet_ops(ECDSAWallet, self.num_iterations)
            
            # Ayrıca imza boyutu listelerini toplamak için yeniden ölçüm yapabiliriz (daha temiz bir yöntem)
            # Ama measure_wallet_ops sadece ortalama döndürüyor. İstersek orada tüm boyutları da döndürelim.
            # Şimdilik basitçe yeniden topluyoruz (performans için ideal değil ama demo için yeterli)
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
        self.progress.setRange(0, 0)  # belirsiz ilerleme
        self.thread = BenchmarkThread(num_iterations=10)
        self.thread.finished.connect(self.on_benchmark_finished)
        self.thread.error.connect(self.on_benchmark_error)
        self.thread.start()
        
    def on_benchmark_finished(self, pq_metrics, ecdsa_metrics, pq_sizes, ecdsa_sizes):
        self.progress.setVisible(False)
        self.btn_run.setEnabled(True)
        
        # Karşılaştırmalı bar grafiği
        bar_canvas = create_comparison_bar_chart(pq_metrics, ecdsa_metrics)
        # İmza boyutları boxplot
        box_canvas = create_signature_size_comparison(pq_sizes, ecdsa_sizes)
        
        # İkisini bir QTabWidget içinde gösterebiliriz
        from PyQt5.QtWidgets import QTabWidget
        tabs = QTabWidget()
        tabs.addTab(bar_canvas, "Karşılaştırma Grafiği")
        tabs.addTab(box_canvas, "İmza Boyutu Dağılımı")
        
        # Eski placeholder'ı kaldır, yenisini ekle
        layout = self.layout()
        layout.replaceWidget(self.canvas_placeholder, tabs)
        self.canvas_placeholder.deleteLater()
        self.canvas_placeholder = tabs
        
        # Detaylı metrikleri de gösteren bir mesaj kutusu eklenebilir
        msg = (f"ML-DSA-44:\n"
               f"  Keygen: {pq_metrics['keygen_time']:.6f} s\n"
               f"  Sign: {pq_metrics['avg_sign_time']:.6f} s\n"
               f"  Verify: {pq_metrics['avg_verify_time']:.6f} s\n"
               f"  Sig size: {pq_metrics['avg_sig_size']:.1f} bytes\n"
               f"ECDSA:\n"
               f"  Keygen: {ecdsa_metrics['keygen_time']:.6f} s\n"
               f"  Sign: {ecdsa_metrics['avg_sign_time']:.6f} s\n"
               f"  Verify: {ecdsa_metrics['avg_verify_time']:.6f} s\n"
               f"  Sig size: {ecdsa_metrics['avg_sig_size']:.1f} bytes")
        QMessageBox.information(self, "Ölçüm Sonuçları", msg)
        
    def on_benchmark_error(self, err_msg):
        self.progress.setVisible(False)
        self.btn_run.setEnabled(True)
        QMessageBox.critical(self, "Hata", f"Ölçüm sırasında hata: {err_msg}")