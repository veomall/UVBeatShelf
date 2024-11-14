from .database_manager import DatabaseManager

class Playlist:
    """
    Класс для управления плейлистами в музыкальной библиотеке.

    Этот класс предоставляет методы для создания, получения, обновления и удаления
    плейлистов, а также для управления треками внутри плейлистов.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует объект Playlist.

        Args:
            db_manager (DatabaseManager): Объект для управления базой данных.
        """
        self.db_manager = db_manager

    def create(self, name: str) -> int:
        """
        Создает новый плейлист.

        Args:
            name (str): Название плейлиста.

        Returns:
            int: ID созданного плейлиста.
        """
        query = "INSERT INTO playlists (name) VALUES (?)"
        return self.db_manager.execute(query, (name,))

    def get(self, playlist_id: int) -> dict:
        """
        Получает информацию о плейлисте по его ID.

        Args:
            playlist_id (int): ID плейлиста.

        Returns:
            dict: Словарь с информацией о плейлисте или None, если плейлист не найден.
        """
        query = "SELECT * FROM playlists WHERE id = ?"
        result = self.db_manager.execute(query, (playlist_id,))
        return result[0] if result else None

    def update(self, playlist_id: int, name: str) -> int:
        """
        Обновляет информацию о плейлисте.

        Args:
            playlist_id (int): ID плейлиста для обновления.
            name (str): Новое название плейлиста.

        Returns:
            int: Количество обновленных строк (обычно 0 или 1).
        """
        query = "UPDATE playlists SET name = ? WHERE id = ?"
        return self.db_manager.execute(query, (name, playlist_id))

    def delete(self, playlist_id: int) -> int:
        """
        Удаляет плейлист.

        Args:
            playlist_id (int): ID плейлиста для удаления.

        Returns:
            int: Количество удаленных строк (обычно 0 или 1).
        """
        query = "DELETE FROM playlists WHERE id = ?"
        return self.db_manager.execute(query, (playlist_id,))

    def add_track(self, playlist_id: int, track_id: int) -> int:
        """
        Добавляет трек в плейлист.

        Args:
            playlist_id (int): ID плейлиста.
            track_id (int): ID трека.
            position (int): Позиция трека в плейлисте.

        Returns:
            int: ID добавленной записи в таблице playlist_tracks.
        """
        # Сначала сдвигаем все существующие треки на одну позицию вниз
        shift_query = """
        UPDATE playlist_tracks
        SET position = position + 1
        WHERE playlist_id = ?
        """
        self.db_manager.execute(shift_query, (playlist_id,))

        # Затем добавляем новый трек на первую позицию
        query = """
        INSERT INTO playlist_tracks (playlist_id, track_id, position)
        VALUES (?, ?, 1)
        """
        return self.db_manager.execute(query, (playlist_id, track_id))

    def remove_track(self, playlist_id: int, track_id: int) -> int:
        """
        Удаляет трек из плейлиста.

        Args:
            playlist_id (int): ID плейлиста.
            track_id (int): ID трека для удаления.

        Returns:
            int: Количество удаленных строк (обычно 0 или 1).
        """
        # Получаем позицию удаляемого трека
        position_query = """
        SELECT position FROM playlist_tracks
        WHERE playlist_id = ? AND track_id = ?
        """
        result = self.db_manager.execute(position_query, (playlist_id, track_id))
        if not result:
            return 0

        position = result[0]['position']

        # Удаляем трек
        delete_query = """
        DELETE FROM playlist_tracks
        WHERE playlist_id = ? AND track_id = ?
        """
        self.db_manager.execute(delete_query, (playlist_id, track_id))

        # Сдвигаем позиции оставшихся треков
        shift_query = """
        UPDATE playlist_tracks
        SET position = position - 1
        WHERE playlist_id = ? AND position > ?
        """
        return self.db_manager.execute(shift_query, (playlist_id, position))
    
    def change_track_position(self, playlist_id: int, track_id: int, new_position: int) -> int:
        # Получаем текущую позицию трека
        current_position_query = """
        SELECT position FROM playlist_tracks
        WHERE playlist_id = ? AND track_id = ?
        """
        result = self.db_manager.execute(current_position_query, (playlist_id, track_id))
        if not result:
            return 0

        current_position = result[0]['position']

        if current_position == new_position:
            return 0  # Позиция не изменилась

        # Обновляем позиции других треков
        if current_position < new_position:
            shift_query = """
            UPDATE playlist_tracks
            SET position = position - 1
            WHERE playlist_id = ? AND position > ? AND position <= ?
            """
            self.db_manager.execute(shift_query, (playlist_id, current_position, new_position))
        else:
            shift_query = """
            UPDATE playlist_tracks
            SET position = position + 1
            WHERE playlist_id = ? AND position >= ? AND position < ?
            """
            self.db_manager.execute(shift_query, (playlist_id, new_position, current_position))

        # Обновляем позицию выбранного трека
        update_query = """
        UPDATE playlist_tracks
        SET position = ?
        WHERE playlist_id = ? AND track_id = ?
        """
        return self.db_manager.execute(update_query, (new_position, playlist_id, track_id))


    def get_tracks(self, playlist_id: int) -> list:
        """
        Получает список треков в плейлисте.

        Args:
            playlist_id (int): ID плейлиста.

        Returns:
            list: Список словарей с информацией о треках в плейлисте.
        """
        query = """
        SELECT t.id, t.title, t.duration, a.name as artist_name, pt.position
        FROM playlist_tracks pt
        JOIN tracks t ON pt.track_id = t.id
        LEFT JOIN artists a ON t.artist_id = a.id
        WHERE pt.playlist_id = ?
        ORDER BY pt.position
        """
        return self.db_manager.execute(query, (playlist_id,))

    def get_info(self, playlist_id: int) -> dict:
        """
        Получает подробную информацию о плейлисте, включая количество треков и общую продолжительность.

        Args:
            playlist_id (int): ID плейлиста.

        Returns:
            dict: Словарь с подробной информацией о плейлисте или None, если плейлист не найден.
        """
        playlist = self.get(playlist_id)
        if playlist:
            tracks = self.get_tracks(playlist_id)
            total_duration = sum(track['duration'] for track in tracks if track['duration'])
            return {
                'id': playlist['id'],
                'name': playlist['name'],
                'track_count': len(tracks),
                'total_duration': self._format_duration(total_duration)
            }
        return None

    def _format_duration(self, duration: int) -> str:
        """
        Форматирует продолжительность в секундах в строку формата "ЧЧ:ММ:СС" или "ММ:СС".

        Args:
            duration (int): Продолжительность в секундах.

        Returns:
            str: Отформатированная строка продолжительности.
        """
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

