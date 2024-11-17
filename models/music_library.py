from .database_manager import DatabaseManager
from .track import Track
from .playlist import Playlist
from .album import Album
from .artist import Artist


class MusicLibrary:
    """
    Класс MusicLibrary представляет собой центральный интерфейс для управления музыкальной библиотекой.
    Он объединяет функциональность работы с треками, плейлистами, альбомами и исполнителями.
    """
    def __init__(self, db_path: str, media_root: str):
        """
        Инициализирует объект MusicLibrary.

        Args:
            db_path (str): Путь к файлу базы данных SQLite.
            media_root (str): Корневая директория для хранения медиафайлов.
        """
        self.db_manager = DatabaseManager(db_path)
        self.media_root = media_root
        self.tracks = Track(self.db_manager, self.media_root)
        self.playlists = Playlist(self.db_manager)
        self.albums = Album(self.db_manager)
        self.artists = Artist(self.db_manager)
    
    def update_db(self) -> None:
        self.db_manager.migrate_database()


    # Методы для работы с треками
    def add_track(self, title: str, file_path: str, cover_path: str = None, artist_id: int = None, album_id: int = None, duration: int = None) -> int:
        """
        Добавляет новый трек в библиотеку.

        Args:
            title (str): Название трека.
            file_path (str): Путь к файлу трека.
            artist_id (int, optional): ID исполнителя.
            album_id (int, optional): Название альбома.
            duration (int, optional): Продолжительность трека в секундах.

        Returns:
            int: ID добавленного трека.
        """
        return self.tracks.add(title, file_path, cover_path, artist_id, album_id, duration)

    def get_track(self, track_id: int) -> dict:
        """Получает информацию о треке по его ID."""
        return self.tracks.get(track_id)

    def get_track_info(self, track_id: int) -> dict:
        """Получает расширенную информацию о треке."""
        return self.tracks.get_info(track_id)

    def update_track(self, track_id: int, **kwargs) -> int:
        """Обновляет информацию о треке."""
        return self.tracks.update(track_id, **kwargs)

    def delete_track(self, track_id: int) -> int:
        """Удаляет трек из библиотеки."""
        return self.tracks.delete(track_id)
    
    def get_all_tracks(self) -> list:
        """Получает список всех треков в библиотеке."""
        return self.tracks.get_all()


    # Методы для работы с плейлистами
    def create_playlist(self, name: str) -> int:
        """Создает новый плейлист."""
        return self.playlists.create(name)

    def get_playlist(self, playlist_id: int) -> dict:
        """Получает информацию о плейлисте."""
        return self.playlists.get(playlist_id)

    def get_playlist_info(self, playlist_id: int) -> dict:
        """Получает расширенную информацию о плейлисте."""
        return self.playlists.get_info(playlist_id)

    def update_playlist(self, playlist_id: int, name: str) -> int:
        """Обновляет название плейлиста."""
        return self.playlists.update(playlist_id, name)

    def delete_playlist(self, playlist_id: int) -> int:
        """Удаляет плейлист."""
        return self.playlists.delete(playlist_id)

    def add_track_to_playlist(self, playlist_id: int, track_id: int) -> int:
        """Добавляет трек в плейлист."""
        return self.playlists.add_track(playlist_id, track_id)

    def remove_track_from_playlist(self, playlist_id: int, track_id: int) -> int:
        """Удаляет трек из плейлиста."""
        return self.playlists.remove_track(playlist_id, track_id)

    def change_track_position_in_playlist(self, playlist_id: int, track_id: int, new_position: int) -> int:
        """Изменяет позицию трека в плейлисте."""
        return self.playlists.change_track_position(playlist_id, track_id, new_position)

    def get_playlist_tracks(self, playlist_id: int) -> list:
        """Получает список треков в плейлисте."""
        return self.playlists.get_tracks(playlist_id)
    
    def get_all_playlists(self) -> list:
        """Получает список всех плейлистов."""
        return self.playlists.get_all()


    # Методы для работы с исполнителями
    def add_artist(self, name: str) -> int:
        """
        Добавляет нового исполнителя или возвращает ID существующего.

        Args:
            name (str): Имя исполнителя.

        Returns:
            int: ID исполнителя.
        """
        existing_artist = self.artists.get_by_name(name)
        if existing_artist:
            return existing_artist['id']
        return self.artists.add(name)

    def get_artist(self, artist_id: int) -> dict:
        """Получает информацию об исполнителе."""
        return self.artists.get(artist_id)

    def get_artist_info(self, artist_id: int) -> dict:
        """Получает расширенную информацию об исполнителе."""
        return self.artists.get_info(artist_id)

    def update_artist(self, artist_id: int, name: str) -> int:
        """Обновляет информацию об исполнителе."""
        return self.artists.update(artist_id, name)

    def delete_artist(self, artist_id: int) -> int:
        """Удаляет исполнителя из библиотеки."""
        return self.artists.delete(artist_id)

    def get_artist_albums(self, artist_id: int) -> list:
        """Получает список альбомов исполнителя."""
        return self.artists.get_albums(artist_id)

    def get_artist_tracks(self, artist_id: int) -> list:
        """Получает список треков исполнителя."""
        return self.artists.get_tracks(artist_id)
    
    def get_all_artists(self) -> list:
        """Получает список всех исполнителей."""
        return self.artists.get_all()
    

    # Методы для работы с альбомами
    def add_album(self, title: str, artist_id: int, year: int = None) -> int:
        """
        Добавляет новый альбом или возвращает ID существующего.

        Args:
            title (str): Название альбома.
            artist_id (int): ID исполнителя.
            year (int, optional): Год выпуска альбома.

        Returns:
            int: ID альбома.
        """
        existing_album = self.albums.get_by_title_and_artist(title, artist_id)
        if existing_album:
            return existing_album['id']
        return self.albums.add(title, artist_id, year)

    def get_album(self, album_id: int) -> dict:
        """Получает информацию об альбоме."""
        return self.albums.get(album_id)

    def get_album_info(self, album_id: int) -> dict:
        """Получает расширенную информацию об альбоме."""
        return self.albums.get_info(album_id)

    def update_album(self, album_id: int, title: str = None, artist_id: int = None, year: int = None) -> int:
        """Обновляет информацию об альбоме."""
        return self.albums.update(album_id, title, artist_id, year)

    def delete_album(self, album_id: int) -> int:
        """Удаляет альбом из библиотеки."""
        return self.albums.delete(album_id)

    def get_album_tracks(self, album_id: int) -> list:
        """Получает список треков в альбоме."""
        return self.albums.get_tracks(album_id)

    def add_track_to_album(self, album_id: int, track_id: int, track_number: int) -> int:
        """Добавляет трек в альбом."""
        return self.albums.add_track(album_id, track_id, track_number)

    def remove_track_from_album(self, track_id: int) -> int:
        """Удаляет трек из альбома."""
        return self.albums.remove_track(track_id)
    
    def get_all_albums_from_artist(self, artist_id: int) -> list:
        """Получает список всех альбомов исполнителя."""
        return self.albums.get_all(artist_id)
    
    def format_duration(self, duration: int) -> str:
        """
        Форматирует продолжительность трека в минуты и секунды.

        Args:
            duration (int): Продолжительность в секундах.

        Returns:
            str: Отформатированная строка продолжительности (MM:SS).
        """
        minutes, seconds = divmod(duration, 60)
        return f"{minutes:02d}:{seconds:02d}"
