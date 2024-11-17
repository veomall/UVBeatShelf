import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_path = "music_library.sqlite"
    media_root = "media"
    
    controller = MainController(db_path, media_root)
    controller.show_window()
    
    sys.exit(app.exec_())