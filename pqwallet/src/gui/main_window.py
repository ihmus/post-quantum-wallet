# src/gui/main_window.py
import sys
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication
from src.gui.wallet_tab import WalletTab
from src.gui.blockchain_tab import BlockchainTab
from src.gui.analytics_tab import AnalyticsTab
from src.gui.comparison_tab import ComparisonTab
from src.blockchain.chain import Blockchain
from src.gui.shor_video_tab import ShorVideoTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Post‑Quantum Blockchain Simülatörü")
        self.setGeometry(100, 100, 1200, 800)

        # Ortak blockchain nesnesi
        self.blockchain = Blockchain(difficulty=2)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Sekmeleri oluştur ve blockchain referansını ver
        self.wallet_tab = WalletTab(self.blockchain)
        self.blockchain_tab = BlockchainTab(self.blockchain)
        self.analytics_tab = AnalyticsTab(self.blockchain)
        self.comparison_tab = ComparisonTab(self.blockchain)
        self.shor_tab = ShorVideoTab()  

        self.tabs.addTab(self.wallet_tab, "💰 Cüzdan")
        self.tabs.addTab(self.blockchain_tab, "🔗 Blockchain")
        self.tabs.addTab(self.analytics_tab, "📊 Analiz")
        self.tabs.addTab(self.comparison_tab, "⚖️ Karşılaştırma")
        self.tabs.addTab(self.shor_tab, "🎥 Tanıtım")

        # Stil
        self.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ccc; }
            QTabBar::tab { padding: 8px; }
            QTableWidget { gridline-color: #ccc; }
        """)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()