from views.main_window import MainWindow
from models.music_library import MusicLibrary

class MainController:
    def __init__(self, db_path, media_root):
        self.music_library = MusicLibrary(db_path, media_root)
        self.view = MainWindow()
        self.view.track_list.itemClicked.connect(self.on_track_clicked)

    def show_window(self):
        self.view.show()
        self.update_track_list()

    def update_track_list(self):
        tracks = self.music_library.get_all_tracks()
        formatted_tracks = [self.music_library.get_track_info(track['id']) for track in tracks]
        self.view.update_track_list(formatted_tracks)
    
    def on_track_clicked(self, item):
        track_widget = self.view.track_list.itemWidget(item)
        if track_widget:
            track_id = track_widget.track['id']
            # Здесь вы можете добавить логику воспроизведения трека
            print(f"Playing track with id: {track_id}")
