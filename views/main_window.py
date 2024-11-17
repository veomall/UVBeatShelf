from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from .track_item import TrackItemWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UVBeatShelf Music Player")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.track_list = QListWidget()
        self.track_list.setSpacing(2)  # Добавляем небольшой отступ между элементами
        layout.addWidget(self.track_list)

    def update_track_list(self, tracks):
        self.track_list.clear()
        for track in tracks:
            track_widget = TrackItemWidget(track)
            item = QListWidgetItem(self.track_list)
            item.setSizeHint(track_widget.sizeHint())
            self.track_list.addItem(item)
            self.track_list.setItemWidget(item, track_widget)

            # Подключаем сигнал play_clicked к слоту (который нужно будет создать в контроллере)
            track_widget.play_clicked.connect(self.on_track_play)

    def on_track_play(self, track_id):
        # Этот метод будет вызываться при нажатии кнопки воспроизведения
        # Здесь вы можете отправить сигнал контроллеру или вызвать соответствующий метод
        print(f"Play track with id: {track_id}")