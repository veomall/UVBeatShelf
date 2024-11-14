from .database_manager import DatabaseManager

class Artist:
    """
    Класс для управления информацией об исполнителях в музыкальной библиотеке.

    Этот класс предоставляет методы для добавления, получения, обновления и удаления
    информации об исполнителях, а также для получения связанных альбомов и треков.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует объект Artist.

        Args:
            db_manager (DatabaseManager): Объект для управления базой данных.
        """
        self.db_manager = db_manager

    def add(self, name: str) -> int:
        """
        Добавляет нового исполнителя в базу данных.

        Args:
            name (str): Имя исполнителя.

        Returns:
            int: ID добавленного исполнителя.
        """
        query = "INSERT INTO artists (name) VALUES (?)"
        return self.db_manager.execute(query, (name,))

    def get(self, artist_id: int) -> dict:
        """
        Получает информацию об исполнителе по его ID.

        Args:
            artist_id (int): ID исполнителя.

        Returns:
            dict: Словарь с информацией об исполнителе или None, если исполнитель не найден.
        """
        query = "SELECT * FROM artists WHERE id = ?"
        result = self.db_manager.execute(query, (artist_id,))
        return result[0] if result else None

    def get_by_name(self, name: str) -> dict:
        """
        Получает информацию об исполнителе по его имени.

        Args:
            name (str): Имя исполнителя.

        Returns:
            dict: Словарь с информацией об исполнителе или None, если исполнитель не найден.
        """
        query = "SELECT * FROM artists WHERE name = ?"
        result = self.db_manager.execute(query, (name,))
        return result[0] if result else None

    def update(self, artist_id: int, name: str) -> int:
        """
        Обновляет информацию об исполнителе.

        Args:
            artist_id (int): ID исполнителя для обновления.
            name (str): Новое имя исполнителя.

        Returns:
            int: Количество обновленных строк (обычно 0 или 1).
        """
        query = "UPDATE artists SET name = ? WHERE id = ?"
        return self.db_manager.execute(query, (name, artist_id))

    def delete(self, artist_id: int) -> int:
        """
        Удаляет исполнителя из базы данных.

        Args:
            artist_id (int): ID исполнителя для удаления.

        Returns:
            int: Количество удаленных строк (обычно 0 или 1).
        """
        query = "DELETE FROM artists WHERE id = ?"
        return self.db_manager.execute(query, (artist_id,))

    def get_all(self) -> list:
        """
        Получает список всех исполнителей.

        Returns:
            list: Список словарей с информацией о всех исполнителях.
        """
        query = "SELECT * FROM artists"
        return self.db_manager.execute(query)

    def get_albums(self, artist_id: int) -> list:
        """
        Получает список альбомов исполнителя.

        Args:
            artist_id (int): ID исполнителя.

        Returns:
            list: Список словарей с информацией об альбомах исполнителя.
        """
        query = "SELECT * FROM albums WHERE artist_id = ?"
        return self.db_manager.execute(query, (artist_id,))

    def get_tracks(self, artist_id: int) -> list:
        """
        Получает список треков исполнителя.

        Args:
            artist_id (int): ID исполнителя.

        Returns:
            list: Список словарей с информацией о треках исполнителя.
        """
        query = "SELECT * FROM tracks WHERE artist_id = ?"
        return self.db_manager.execute(query, (artist_id,))

    def get_info(self, artist_id: int) -> dict:
        """
        Получает подробную информацию об исполнителе, включая количество альбомов и треков.

        Args:
            artist_id (int): ID исполнителя.

        Returns:
            dict: Словарь с подробной информацией об исполнителе или None, если исполнитель не найден.
        """
        artist = self.get(artist_id)
        if artist:
            albums = self.get_albums(artist_id)
            tracks = self.get_tracks(artist_id)
            return {
                'id': artist['id'],
                'name': artist['name'],
                'albums_count': len(albums),
                'tracks_count': len(tracks)
            }
        return None

