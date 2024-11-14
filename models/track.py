import os
import shutil
import uuid
from .database_manager import DatabaseManager

class Track:
    """
    Класс для управления треками в музыкальной библиотеке.

    Этот класс предоставляет методы для добавления, получения, обновления и удаления
    информации о треках, а также для управления связанными файлами.
    """
    def __init__(self, db_manager: DatabaseManager, media_root: str):
        """
        Инициализирует объект Track.

        Args:
            db_manager (DatabaseManager): Объект для управления базой данных.
            media_root (str): Корневая директория для хранения медиафайлов.
        """
        self.db_manager = db_manager
        self.media_root = media_root
        self.audio_folder = os.path.join(self.media_root, 'audio')
        self.covers_folder = os.path.join(self.media_root, 'covers')
        self._create_media_structure()

    def add(self, title: str, file_path: str, cover_path: str = None, artist_id: int = None, album_id: int = None, duration: int = None, lyrics: str = None) -> int:
        """
        Добавляет новый трек в базу данных.

        Args:
            title (str): Название трека.
            file_path (str): Путь к файлу трека.
            cover_path (str, optional): Путь к файлу обложки.
            artist_id (int, optional): ID исполнителя.
            album_id (int, optional): ID альбома.
            duration (int, optional): Продолжительность трека в секундах.
            lyrics (str, optional): Текст трека.

        Returns:
            int: ID добавленного трека.
        """
        new_file_path = self._copy_to_audio_folder(file_path)
        new_cover_path = self._copy_to_covers_folder(cover_path) if cover_path else None

        query = """
        INSERT INTO tracks (title, artist_id, album_id, duration, file_path, cover_path, lyrics)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.db_manager.execute(query, (title, artist_id, album_id, duration, new_file_path, new_cover_path, lyrics))

    def get(self, track_id: int) -> dict:
        """
        Получает информацию о треке по его ID.

        Args:
            track_id (int): ID трека.

        Returns:
            dict: Словарь с информацией о треке или None, если трек не найден.
        """
        query = """
        SELECT t.*, a.name as artist_name, al.title as album_title
        FROM tracks t
        LEFT JOIN artists a ON t.artist_id = a.id
        LEFT JOIN albums al ON t.album_id = al.id
        WHERE t.id = ?
        """
        result = self.db_manager.execute(query, (track_id,))
        return result[0] if result else None

    def get_info(self, track_id: int) -> dict:
        """
        Получает подробную информацию о треке.

        Args:
            track_id (int): ID трека.

        Returns:
            dict: Словарь с подробной информацией о треке или None, если трек не найден.
        """
        query = """
        SELECT t.id, t.title, t.duration, t.file_path, t.cover_path, t.lyrics,
               a.name as artist_name, al.title as album_title
        FROM tracks t
        LEFT JOIN artists a ON t.artist_id = a.id
        LEFT JOIN albums al ON t.album_id = al.id
        WHERE t.id = ?
        """
        result = self.db_manager.execute(query, (track_id,))
        if result:
            track = result[0]
            return {
                'id': track['id'],
                'title': track['title'],
                'artist': track['artist_name'] or 'Unknown Artist',
                'album': track['album_title'] or 'Unknown Album',
                'duration': self._format_duration(track['duration']),
                'file_path': track['file_path'],
                'cover_path': track['cover_path'],
                'lyrics': track['lyrics'] or 'No lyrics provided'
            }
        return None

    def update(self, track_id: int, title: str = None, artist_id: int = None, album_id: int = None, duration: int = None, lyrics: str = None) -> int:
        """
        Обновляет информацию о треке.

        Args:
            track_id (int): ID трека для обновления.
            title (str, optional): Новое название трека.
            artist_id (int, optional): Новый ID исполнителя.
            album_id (int, optional): Новый ID альбома.
            duration (int, optional): Новая продолжительность трека в секундах.

        Returns:
            int: Количество обновленных строк (обычно 0 или 1).
        """
        update_fields = []
        parameters = []
        if title:
            update_fields.append("title = ?")
            parameters.append(title)
        if artist_id is not None:
            update_fields.append("artist_id = ?")
            parameters.append(artist_id)
        if album_id is not None:
            update_fields.append("album_id = ?")
            parameters.append(album_id)
        if duration is not None:
            update_fields.append("duration = ?")
            parameters.append(duration)
        if lyrics is not None:
            update_fields.append("lyrics = ?")
            parameters.append(lyrics)

        if not update_fields:
            return 0

        query = f"UPDATE tracks SET {', '.join(update_fields)} WHERE id = ?"
        parameters.append(track_id)
        return self.db_manager.execute(query, tuple(parameters))

    def delete(self, track_id: int) -> int:
        """
        Удаляет трек из базы данных и его файлы.

        Args:
            track_id (int): ID трека для удаления.

        Returns:
            int: Количество удаленных строк (обычно 0 или 1).
        """
        track = self.get(track_id)
        if track:
            if os.path.exists(track['file_path']):
                os.remove(track['file_path'])
            if track['cover_path'] and os.path.exists(track['cover_path']):
                os.remove(track['cover_path'])
        query = "DELETE FROM tracks WHERE id = ?"
        return self.db_manager.execute(query, (track_id,))

    def _create_media_structure(self):
        """Создает структуру медиа-папки с подпапками для аудио и обложек."""
        os.makedirs(self.audio_folder, exist_ok=True)
        os.makedirs(self.covers_folder, exist_ok=True)

    def _copy_to_audio_folder(self, file_path: str) -> str:
        """Копирует аудиофайл в папку аудио."""
        _, ext = os.path.splitext(file_path)
        new_filename = f"{uuid.uuid4()}{ext}"
        new_file_path = os.path.join(self.audio_folder, new_filename)
        shutil.copy2(file_path, new_file_path)
        return new_file_path

    def _copy_to_covers_folder(self, cover_path: str) -> str:
        """Копирует файл обложки в папку обложек."""
        _, ext = os.path.splitext(cover_path)
        new_filename = f"{uuid.uuid4()}{ext}"
        new_file_path = os.path.join(self.covers_folder, new_filename)
        shutil.copy2(cover_path, new_file_path)
        return new_file_path

    def _get_or_create_artist(self, artist_name: str) -> int:
        """
        Получает ID исполнителя или создает нового, если не существует.

        Args:
            artist_name (str): Имя исполнителя.

        Returns:
            int: ID исполнителя.
        """
        query = "SELECT id FROM artists WHERE name = ?"
        result = self.db_manager.execute(query, (artist_name,))
        if result:
            return result[0]['id']
        else:
            return self.db_manager.execute("INSERT INTO artists (name) VALUES (?)", (artist_name,))

    def _get_or_create_album(self, album_title: str, artist_id: int = None) -> int:
        """
        Получает ID альбома или создает новый, если не существует.

        Args:
            album_title (str): Название альбома.
            artist_id (int, optional): ID исполнителя альбома.

        Returns:
            int: ID альбома.
        """
        query = "SELECT id FROM albums WHERE title = ? AND artist_id = ?"
        result = self.db_manager.execute(query, (album_title, artist_id))
        if result:
            return result[0]['id']
        else:
            return self.db_manager.execute("INSERT INTO albums (title, artist_id) VALUES (?, ?)", (album_title, artist_id))

    def _format_duration(self, duration: int) -> str:
        """
        Форматирует продолжительность трека в минуты и секунды.

        Args:
            duration (int): Продолжительность в секундах.

        Returns:
            str: Отформатированная строка продолжительности (MM:SS).
        """
        minutes, seconds = divmod(duration, 60)
        return f"{minutes:02d}:{seconds:02d}"

