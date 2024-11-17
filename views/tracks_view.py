from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from .track_item import TrackItemWidget

class TracksView(QWidget):
    track_play_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.track_list = QListWidget()
        self.track_list.setSpacing(2)
        layout.addWidget(self.track_list)

    def update_tracks(self, tracks):
        self.track_list.clear()
        for track in tracks:
            track_widget = TrackItemWidget(track)
            item = QListWidgetItem(self.track_list)
            item.setSizeHint(track_widget.sizeHint())
            self.track_list.addItem(item)
            self.track_list.setItemWidget(item, track_widget)
            track_widget.play_clicked.connect(self.track_play_requested.emit)