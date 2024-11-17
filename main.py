import sys
from models.music_library import MusicLibrary
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_path = "music_library.sqlite"
    media_root = "media"
    music_library = MusicLibrary(db_path, media_root)

    controller = MainController(music_library)
    controller.show_window()

    sys.exit(app.exec_())
