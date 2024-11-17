from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from .tracks_view import TracksView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UVBeatShelf Music Player")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.tracks_view = TracksView()
        layout.addWidget(self.tracks_view)

        # Подключаем сигнал track_play_requested к слоту on_track_play
        self.tracks_view.track_play_requested.connect(self.on_track_play)

    def update_track_list(self, tracks):
        self.tracks_view.update_tracks(tracks)

    def on_track_play(self, track_id):
        print(f"Play track with id: {track_id}")
