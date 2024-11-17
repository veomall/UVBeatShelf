from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from .tracks_view import TracksView
from .player_widget import PlayerWidget

class MainWindow(QMainWindow):
    play_track = pyqtSignal(int)
    resume_track = pyqtSignal()
    pause_track = pyqtSignal()
    seek_track = pyqtSignal(int)

    def __init__(self, music_library):
        super().__init__()
        self.setWindowTitle("UVBeatShelf Music Player")
        self.setGeometry(100, 100, 800, 600)
        self.music_library = music_library

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.tracks_view = TracksView(self.music_library)
        layout.addWidget(self.tracks_view)

        self.player_widget = PlayerWidget()
        layout.addWidget(self.player_widget)

        # Подключаем сигналы
        self.tracks_view.track_play_requested.connect(self.on_track_play)
        self.player_widget.play_pause_clicked.connect(self.on_play_pause)
        self.player_widget.seek_changed.connect(self.on_seek)

    def update_track_list(self, tracks):
        self.tracks_view.update_tracks(tracks)

    def on_track_play(self, track_id):
        self.play_track.emit(track_id)

    def on_play_pause(self, is_play):
        if is_play:
            self.play_track.emit(None)  # Возобновить текущий трек
        else:
            self.pause_track.emit()

    def on_seek(self, position):
        self.seek_track.emit(position)

    def update_player_position(self, position):
        self.player_widget.update_position(position)

    def set_track_duration(self, duration):
        self.player_widget.set_duration(duration)
