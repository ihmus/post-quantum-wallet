# src/gui/blockchain_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QTabWidget, QHeaderView, QLabel)
from PyQt5.QtCore import Qt

class BlockchainTab(QWidget):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain
        self.init_ui()
        self.refresh()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Blok #", "Hash", "İşlem Sayısı", "Zaman"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QLabel("BLOCKCHAIN ZİNCİRİ"))
        layout.addWidget(self.table)
        self.setLayout(layout)

    def refresh(self):
        """Blockchain verilerini tabloya yükler."""
        chain = self.blockchain.chain
        self.table.setRowCount(len(chain))
        for i, block in enumerate(chain):
            self.table.setItem(i, 0, QTableWidgetItem(str(block.index)))
            self.table.setItem(i, 1, QTableWidgetItem(block.hash[:16] + "..."))
            self.table.setItem(i, 2, QTableWidgetItem(str(len(block.transactions))))
            self.table.setItem(i, 3, QTableWidgetItem(str(block.timestamp)))
        # İleri seviye: blok tıklanınca işlemleri göster
        self.table.cellDoubleClicked.connect(self.show_block_details)

    def show_block_details(self, row, col):
        block = self.blockchain.chain[row]
        tx_list = "\n".join([f"  {tx.sender[:8]} -> {tx.recipient[:8]} : {tx.amount}" for tx in block.transactions])
        msg = f"Blok #{block.index}\nHash: {block.hash}\nİşlemler:\n{tx_list if tx_list else '  (işlem yok)'}"
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Blok Detayı", msg)
    def showEvent(self, event):
        self.refresh()
        super().showEvent(event)