from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

class TrackItemWidget(QWidget):
    play_clicked = pyqtSignal(int)  # Сигнал, который будет отправлен при нажатии кнопки воспроизведения

    def __init__(self, track, parent=None):
        super().__init__(parent)
        self.track = track
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Обложка трека
        cover_label = QLabel()
        cover_label.setFixedSize(50, 50)
        cover_path = self.track['cover_path']
        cover_image = QPixmap(cover_path if cover_path else "utils/images/cover-image.png")
        cover_image = cover_image.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        cover_label.setPixmap(cover_image)
        cover_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(cover_label)

        # Название трека
        title_label = QLabel(self.track['title'])
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label)

        # Исполнитель
        artist_label = QLabel(self.track['artist'])
        layout.addWidget(artist_label)

        # Длительность трека
        duration_label = QLabel(self.track['duration'])
        layout.addWidget(duration_label)

        # Кнопка воспроизведения
        play_button = QPushButton()
        play_button.setFixedSize(30, 30)
        play_icon = QIcon("utils/images/play-button.png")
        play_button.setIcon(play_icon)
        play_button.setIconSize(play_button.size())
        play_button.clicked.connect(self.on_play_clicked)
        layout.addWidget(play_button)

        layout.setStretch(0, 0)  # Обложка трека не растягивается
        layout.setStretch(1, 2)  # Название трека занимает больше места
        layout.setStretch(2, 1)  # Исполнитель занимает меньше места
        layout.setStretch(3, 0)  # Длительность трека не растягивается
        layout.setStretch(4, 0)  # Кнопка воспроизведения не растягивается

    def on_play_clicked(self):
        self.play_clicked.emit(self.track['id'])