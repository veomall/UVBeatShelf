from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from .track_item import TrackItemWidget

class TracksView(QWidget):
    track_play_requested = pyqtSignal(int)

    def __init__(self, music_library, parent=None):
        super().__init__(parent)
        self.music_library = music_library
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.track_list = QListWidget()
        self.track_list.setSpacing(2)
        layout.addWidget(self.track_list)

    def update_tracks(self, tracks):
        self.track_list.clear()
        for track in tracks:
            formatted_track = {
                'id': track['id'],
                'title': track['title'],
                'artist': self.music_library.get_artist(track['artist_id'])['name'],
                'duration': self.music_library.format_duration(track['duration']),
                'cover_path': track['cover_path']
            }
            track_widget = TrackItemWidget(formatted_track)
            item = QListWidgetItem(self.track_list)
            item.setSizeHint(track_widget.sizeHint())
            self.track_list.addItem(item)
            self.track_list.setItemWidget(item, track_widget)
            track_widget.play_clicked.connect(self.track_play_requested.emit)