from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QPushButton,
    QLabel,
    QTextBrowser,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


@dataclass
class MediaPack:
    video_url: str
    title: str = "Tanıtım Videosu"
    description: str = "Buraya videonun tanıtım metnini yazabilirsin."
    bottom_text: str = "Videonun altına ek açıklama yazısı eklenebilir."


class ShorVideoTab(QWidget):
    """Tanıtım yazısı + video + açıklama düzeni."""

    def __init__(self, media: Optional[MediaPack] = None, parent=None):
        super().__init__(parent)

        self.media = media or MediaPack(
            video_url="file:///home/ihmus/Belgeler/GitHub/post-quantum-wallet/pq.mp4",
            title="Post Quantum Wallet",
            description=(
                "Bu bölümde videonun kısa tanıtımını, özelliklerini ve açıklama metnini "
                "gösterebilirsin."
            ),
            bottom_text=(
                "Buraya video ile ilgili ikinci açıklama alanını koyabilirsin. "
                "Özellik listesi, notlar veya kısa destek metinleri için uygundur."
            ),
        )

        self._build_ui()
        self._build_player()
        self._connect_signals()
        self._load_media(self.media)

    def _build_ui(self) -> None:
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(12, 12, 12, 12)
        self.root_layout.setSpacing(12)

        self.title_label = QLabel(self.media.title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        self.root_layout.addWidget(self.title_label)

        # Ana sayfa düzeni: video solda, metin sağda, ek metin altta
        page = QVBoxLayout()
        page.setSpacing(12)

        top_row = QGridLayout()
        top_row.setHorizontalSpacing(12)
        top_row.setVerticalSpacing(12)

        # Video kartı
        self.video_card = QFrame(self)
        self.video_card.setObjectName("videoCard")
        video_card_layout = QVBoxLayout(self.video_card)
        video_card_layout.setContentsMargins(0, 0, 0, 0)
        video_card_layout.setSpacing(0)

        self.video_widget = QVideoWidget(self.video_card)
        self.video_widget.setMinimumSize(QSize(640, 360))
        video_card_layout.addWidget(self.video_widget)

        # Videonun sol üstünde yarı saydam kontrol barı
        self.overlay_bar = QWidget(self.video_widget)
        self.overlay_bar.setAttribute(Qt.WA_TranslucentBackground, True)
        self.overlay_bar.setStyleSheet("background: transparent;")

        overlay_layout = QHBoxLayout(self.overlay_bar)
        overlay_layout.setContentsMargins(8, 8, 8, 8)
        overlay_layout.setSpacing(8)

        self.btn_play = QPushButton("▶", self.overlay_bar)
        self.btn_mute = QPushButton("🔊", self.overlay_bar)

        for btn in (self.btn_play, self.btn_mute):
            btn.setFixedSize(42, 42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 130);
                    color: white;
                    border: none;
                    border-radius: 21px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 190);
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 220);
                }
            """)

        overlay_layout.addWidget(self.btn_play)
        overlay_layout.addWidget(self.btn_mute)
        overlay_layout.addStretch(1)
        self.overlay_bar.raise_()

        top_row.addWidget(self.video_card, 0, 0, 1, 2)

        self.info_box = QTextBrowser(self)
        self.info_box.setObjectName("infoBox")
        self.info_box.setOpenExternalLinks(True)
        self.info_box.setText(self.media.description)
        top_row.addWidget(self.info_box, 0, 2)

        page.addLayout(top_row)

        self.bottom_box = QTextBrowser(self)
        self.bottom_box.setObjectName("bottomBox")
        self.bottom_box.setOpenExternalLinks(True)
        self.bottom_box.setText(self.media.bottom_text)
        page.addWidget(self.bottom_box)

        self.root_layout.addLayout(page)

        self.setStyleSheet("""
            # titleLabel {
                font-size: 22px;
                font-weight: 700;
                padding: 4px 2px;
            }
            # videoCard {
                background: #000;
                border-radius: 12px;
                overflow: hidden;
            }
            # infoBox, # bottomBox {
                border: 1px solid rgba(0, 0, 0, 30);
                border-radius: 12px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.92);
                font-size: 14px;
            }
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._place_overlay()

    def _place_overlay(self):
        if not hasattr(self, "overlay_bar"):
            return
        self.overlay_bar.adjustSize()
        margin = 10
        self.overlay_bar.move(margin, margin)

    def _build_player(self) -> None:
        self.video_player = QMediaPlayer(self)
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.setMuted(False)
        self.video_player.setVolume(100)

    def _connect_signals(self) -> None:
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_mute.clicked.connect(self.toggle_mute)

        self.video_player.stateChanged.connect(self._on_state_changed)
        self.video_player.mediaStatusChanged.connect(self._on_media_status_changed)
        self.video_player.error.connect(self._on_error)

    def _load_media(self, media: MediaPack) -> None:
        self.media = media
        self.title_label.setText(media.title)
        self.info_box.setText(media.description)
        self.bottom_box.setText(media.bottom_text)
        self.video_player.setMedia(QMediaContent(QUrl(media.video_url)))
        self._update_buttons()

    def toggle_play(self) -> None:
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.video_player.pause()
        else:
            self.video_player.play()
        self._update_buttons()

    def toggle_mute(self) -> None:
        self.video_player.setMuted(not self.video_player.isMuted())
        self._update_buttons()

    def _update_buttons(self) -> None:
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.btn_play.setText("⏸")
        else:
            self.btn_play.setText("▶")

        self.btn_mute.setText("🔇" if self.video_player.isMuted() else "🔊")

    def _on_state_changed(self, _state: QMediaPlayer.State) -> None:
        self._update_buttons()

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.EndOfMedia:
            self._update_buttons()

    def _on_error(self, *_args) -> None:
        err = self.video_player.errorString()
        if err:
            print("Video error:", err)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    demo = ShorVideoTab(
        MediaPack(
            video_url="file:///home/ihmus/Belgeler/GitHub/post-quantum-wallet/pq.mp4",
            title="Post Quantum Wallet",
            description="Sağ tarafta videonun kısa tanıtımı yer alır. Video solda durur.",
            bottom_text="Alt kısımda ek açıklamalar, özellikler veya kısa notlar gösterilebilir.",
        )
    )
    demo.resize(1200, 800)
    demo.show()

    app.exec_()