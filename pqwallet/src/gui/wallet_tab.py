# src/gui/wallet_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QRadioButton, QPushButton, QLabel, QLineEdit,
                             QTextEdit, QMessageBox)
from src.wallet.pq_wallet import PQWallet
from src.wallet.ecdsa_wallet import ECDSAWallet
from src.blockchain.models import Transaction

class WalletTab(QWidget):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain
        self.pq_wallet = None
        self.ecdsa_wallet = None
        self.current_wallet_type = "pq"
        self.current_wallet = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Cüzdan tipi
        type_group = QGroupBox("Cüzdan Tipi")
        type_layout = QHBoxLayout()
        self.rb_pq = QRadioButton("Post‑Quantum (ML-DSA-44)")
        self.rb_ecdsa = QRadioButton("ECDSA (secp256k1)")
        self.rb_pq.setChecked(True)
        self.rb_pq.toggled.connect(self.on_wallet_type_changed)
        type_layout.addWidget(self.rb_pq)
        type_layout.addWidget(self.rb_ecdsa)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Cüzdan oluşturma
        self.btn_create = QPushButton("🆕 Yeni Cüzdan Oluştur")
        self.btn_create.clicked.connect(self.create_wallet)
        layout.addWidget(self.btn_create)

        # Bilgiler
        info_group = QGroupBox("Cüzdan Bilgileri")
        info_layout = QVBoxLayout()
        self.lbl_address = QLabel("Adres: -")
        self.lbl_pubkey_size = QLabel("Açık Anahtar Boyutu: -")
        self.lbl_balance = QLabel("Bakiye: 100 PQCoin (simülasyon)")
        info_layout.addWidget(self.lbl_address)
        info_layout.addWidget(self.lbl_pubkey_size)
        info_layout.addWidget(self.lbl_balance)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Transfer
        transfer_group = QGroupBox("Coin Gönder")
        transfer_layout = QVBoxLayout()
        self.txt_recipient = QLineEdit()
        self.txt_recipient.setPlaceholderText("Alıcı adresi")
        self.txt_amount = QLineEdit()
        self.txt_amount.setPlaceholderText("Miktar")
        self.btn_send = QPushButton("💸 Gönder ve Havuza Ekle")
        self.btn_send.clicked.connect(self.send_transaction)
        transfer_layout.addWidget(QLabel("Alıcı Adresi:"))
        transfer_layout.addWidget(self.txt_recipient)
        transfer_layout.addWidget(QLabel("Miktar:"))
        transfer_layout.addWidget(self.txt_amount)
        transfer_layout.addWidget(self.btn_send)
        transfer_group.setLayout(transfer_layout)
        layout.addWidget(transfer_group)

        # Madencilik
        self.btn_mine = QPushButton("⛏️ Madencilik Yap (Blok Üret)")
        self.btn_mine.clicked.connect(self.mine_block)
        layout.addWidget(self.btn_mine)

        # Sonuç alanı
        self.txt_result = QTextEdit()
        self.txt_result.setReadOnly(True)
        self.txt_result.setMaximumHeight(150)
        layout.addWidget(QLabel("Sonuç:"))
        layout.addWidget(self.txt_result)

        self.setLayout(layout)

    def on_wallet_type_changed(self):
        self.current_wallet_type = "pq" if self.rb_pq.isChecked() else "ecdsa"
        self.current_wallet = None
        self.lbl_address.setText("Adres: -")
        self.lbl_pubkey_size.setText("Açık Anahtar Boyutu: -")

    def create_wallet(self):
        if self.current_wallet_type == "pq":
            self.current_wallet = PQWallet()
        else:
            self.current_wallet = ECDSAWallet()
        self.current_wallet.generate_keypair()
        self.lbl_address.setText(f"Adres: {self.current_wallet.get_address()}")
        pubkey = self.current_wallet.public_key
        self.lbl_pubkey_size.setText(f"Açık Anahtar Boyutu: {len(pubkey)} bayt")
        self.txt_result.append("✅ Yeni cüzdan oluşturuldu.")

    def send_transaction(self):
        if self.current_wallet is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir cüzdan oluşturun!")
            return
        recipient = self.txt_recipient.text().strip()
        amount_text = self.txt_amount.text().strip()
        if not recipient or not amount_text:
            QMessageBox.warning(self, "Uyarı", "Alıcı adresi ve miktar girin!")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Miktar sayı olmalı!")
            return

        tx = Transaction(sender=self.current_wallet.get_address(),
                         recipient=recipient,
                         amount=amount,
                         wallet=self.current_wallet,
                         wallet_type=self.current_wallet_type)
        tx.sign(self.current_wallet)
        if tx.is_valid():
            if self.blockchain.add_transaction(tx):
                self.txt_result.append(f"💰 {amount} coin {recipient[:8]}... adresine gönderildi ve havuza eklendi.")
                self.txt_result.append(f"   İmza boyutu: {len(tx.signature)} bayt")
                self.txt_recipient.clear()
                self.txt_amount.clear()
                # Blockchain sekmesini güncellemek için sinyal gönderilebilir (ileride)
            else:
                self.txt_result.append("❌ İşlem geçersiz (doğrulama hatası).")
        else:
            self.txt_result.append("❌ İşlem imzası geçersiz!")

    def mine_block(self):
        if not self.blockchain.pending_transactions:
            self.txt_result.append("⚠️ Havuzda işlem yok, madencilik yapılamaz.")
            return
        self.txt_result.append("⛏️ Madencilik başlıyor...")
        new_block = self.blockchain.mine_pending_transactions()
        if new_block:
            self.txt_result.append(f"✅ Yeni blok (#{new_block.index}) eklendi. Hash: {new_block.hash[:16]}...")
            # Blockchain tablosunu yenilemek için sinyal mekanizması kurulabilir.
        else:
            self.txt_result.append("❌ Madencilik başarısız.")