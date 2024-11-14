from .database_manager import DatabaseManager

class Album:
    """
    Класс для управления альбомами в музыкальной библиотеке.

    Этот класс предоставляет методы для добавления, получения, обновления и удаления
    альбомов, а также для получения связанных треков и информации об альбоме.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует объект Album.

        Args:
            db_manager (DatabaseManager): Объект для управления базой данных.
        """
        self.db_manager = db_manager

    def add(self, title: str, artist_id: int, year: int = None) -> int:
        """
        Добавляет новый альбом в базу данных.

        Args:
            title (str): Название альбома.
            artist_id (int): ID исполнителя альбома.
            year (int, optional): Год выпуска альбома. По умолчанию None.

        Returns:
            int: ID добавленного альбома.
        """
        query = "INSERT INTO albums (title, artist_id, year) VALUES (?, ?, ?)"
        return self.db_manager.execute(query, (title, artist_id, year))

    def get(self, album_id: int) -> dict:
        """
        Получает информацию об альбоме по его ID.

        Args:
            album_id (int): ID альбома.

        Returns:
            dict: Словарь с информацией об альбоме или None, если альбом не найден.
        """
        query = "SELECT * FROM albums WHERE id = ?"
        result = self.db_manager.execute(query, (album_id,))
        return result[0] if result else None

    def get_by_title_and_artist(self, title: str, artist_id: int) -> dict:
        """
        Получает информацию об альбоме по его названию и ID исполнителя.

        Args:
            title (str): Название альбома.
            artist_id (int): ID исполнителя.

        Returns:
            dict: Словарь с информацией об альбоме или None, если альбом не найден.
        """
        query = "SELECT * FROM albums WHERE title = ? AND artist_id = ?"
        result = self.db_manager.execute(query, (title, artist_id))
        return result[0] if result else None

    def update(self, album_id: int, title: str = None, artist_id: int = None, year: int = None) -> int:
        """
        Обновляет информацию об альбоме.

        Args:
            album_id (int): ID альбома для обновления.
            title (str, optional): Новое название альбома.
            artist_id (int, optional): Новый ID исполнителя.
            year (int, optional): Новый год выпуска.

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
        if year is not None:
            update_fields.append("year = ?")
            parameters.append(year)

        if not update_fields:
            return 0

        query = f"UPDATE albums SET {', '.join(update_fields)} WHERE id = ?"
        parameters.append(album_id)
        return self.db_manager.execute(query, tuple(parameters))

    def delete(self, album_id: int) -> int:
        """
        Удаляет альбом из базы данных.

        Args:
            album_id (int): ID альбома для удаления.

        Returns:
            int: Количество удаленных строк (обычно 0 или 1).
        """
        query = "DELETE FROM albums WHERE id = ?"
        return self.db_manager.execute(query, (album_id,))

    def get_all(self, artist_id: int) -> list:
        """
        Получает список всех альбомов определенного исполнителя.
        """
        query = "SELECT * FROM albums WHERE artist_id =?"
        return self.db_manager.execute(query, (artist_id,))

    def get_tracks(self, album_id: int) -> list:
        """
        Получает список всех треков для заданного альбома.

        Args:
            album_id (int): ID альбома.

        Returns:
            list: Список словарей с информацией о треках альбома.
        """
        query = "SELECT * FROM tracks WHERE album_id = ?"
        return self.db_manager.execute(query, (album_id,))

    def get_info(self, album_id: int) -> dict:
        """
        Получает подробную информацию об альбоме, включая количество треков и имя исполнителя.

        Args:
            album_id (int): ID альбома.

        Returns:
            dict: Словарь с подробной информацией об альбоме или None, если альбом не найден.
        """
        query = """
        SELECT al.id, al.title, al.year, a.name as artist_name,
               COUNT(t.id) as track_count
        FROM albums al
        LEFT JOIN artists a ON al.artist_id = a.id
        LEFT JOIN tracks t ON t.album_id = al.id
        WHERE al.id = ?
        GROUP BY al.id
        """
        result = self.db_manager.execute(query, (album_id,))
        if result:
            album = result[0]
            return {
                'id': album['id'],
                'title': album['title'],
                'artist': album['artist_name'] or 'Unknown Artist',
                'year': album['year'] or 'Unknown Year',
                'track_count': album['track_count']
            }
        return None

