from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import Qt, pyqtSignal

class PlayerWidget(QWidget):
    play_pause_clicked = pyqtSignal(bool)  # True для play, False для pause
    seek_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.clicked.connect(self.on_play_pause_clicked)
        layout.addWidget(self.play_pause_button)

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 100)
        self.seek_slider.sliderMoved.connect(self.on_seek_changed)
        layout.addWidget(self.seek_slider)

    def on_play_pause_clicked(self):
        is_playing = self.play_pause_button.text() == "Pause"
        self.play_pause_button.setText("Play" if is_playing else "Pause")
        self.play_pause_clicked.emit(not is_playing)

    def on_seek_changed(self, value):
        self.seek_changed.emit(value)

    def set_duration(self, duration):
        self.seek_slider.setRange(0, int(duration))

    def update_position(self, position):
        self.seek_slider.setValue(position)