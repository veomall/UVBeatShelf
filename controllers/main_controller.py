from views.main_window import MainWindow
from models.music_library import MusicLibrary

class MainController:
    def __init__(self, db_path, media_root):
        self.music_library = MusicLibrary(db_path, media_root)
        self.view = MainWindow()

    def show_window(self):
        self.view.show()
        self.update_track_list()

    def update_track_list(self):
        tracks = self.music_library.get_all_tracks()
        formatted_tracks = [self.music_library.get_track_info(track['id']) for track in tracks]
        self.view.update_track_list(formatted_tracks)

    def on_track_play(self, track_id):
        # Здесь вы можете добавить логику воспроизведения трека
        print(f"Playing track with id: {track_id}")
