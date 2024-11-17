from views.main_window import MainWindow
from PyQt5.QtCore import QTimer

class MainController:
    def __init__(self, music_library):
        self.music_library = music_library
        self.view = MainWindow(self.music_library)

        # Подключаем сигналы
        self.view.play_track.connect(self.play_track)
        self.view.pause_track.connect(self.pause_track)
        self.view.seek_track.connect(self.seek_track)

        # Создаем таймер для обновления позиции плеера
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_player_position)
        self.update_timer.start(1000)  # Обновляем каждую секунду

        self.current_track_id = None
        self.is_playing = False
        self.current_position = 0
    def show_window(self):
        self.view.show()
        self.update_track_list()

    def update_track_list(self):
        tracks = self.music_library.get_all_tracks()
        self.view.update_track_list(tracks)

    def play_track(self, track_id):
        if track_id is not None:
            self.current_track_id = track_id
            self.current_position = 0
        if self.current_track_id:
            # Здесь должна быть логика воспроизведения трека
            print(f"Playing track with id: {self.current_track_id}")
            self.is_playing = True
            track_info = self.music_library.get_track(self.current_track_id)
            if track_info is not None:
                self.view.set_track_duration(track_info.get('duration', 0))
            else:
                print(f"Error: Track with id {self.current_track_id} not found")
                self.is_playing = False
                self.current_track_id = None

    def pause_track(self):
        if self.is_playing:
            # Здесь должна быть логика паузы трека
            print("Pausing track")
            self.is_playing = False

    def seek_track(self, position):
        if self.current_track_id:
            # Здесь должна быть логика перемотки трека
            print(f"Seeking to position: {position}")
            self.current_position = position

    def update_player_position(self):
        if self.is_playing:
            self.current_position += 1
            self.view.update_player_position(self.current_position)
