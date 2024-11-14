import sqlite3
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any, Union


class DatabaseManager:
    """
    Класс для управления базой данных SQLite.

    Этот класс предоставляет методы для выполнения SQL-запросов,
    создания таблиц и управления структурой базы данных.
    """
    def __init__(self, db_path: str):
        """
        Инициализирует менеджер базы данных.

        Args:
            db_path (str): Путь к файлу базы данных SQLite.
        """
        self.db_path = db_path
        self.create_tables()

    def execute(self, query: str, parameters: tuple = ()) -> Union[List[Dict[str, Any]], int]:
        """
        Выполняет SQL-запрос к базе данных.

        Args:
            query (str): SQL-запрос для выполнения.
            parameters (tuple, optional): Параметры для SQL-запроса. По умолчанию пустой кортеж.

        Returns:
            Union[List[Dict[str, Any]], int]: Результат запроса. 
            Для SELECT-запросов возвращает список словарей с данными.
            Для других запросов возвращает количество затронутых строк или последний вставленный ID.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            try:
                cursor.execute(query, parameters)
                if query.strip().upper().startswith("SELECT"):
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                conn.rollback()
                return []

    def create_tables(self):
        """
        Создает необходимые таблицы в базе данных, если они еще не существуют.

        Создает таблицы для артистов, альбомов, треков, плейлистов и связей между плейлистами и треками.
        """
        # Создание таблицы артистов
        self.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        # Создание таблицы альбомов
        self.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist_id INTEGER,
                year INTEGER,
                FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE SET NULL
            )
        ''')

        # Создание таблицы треков
        self.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist_id INTEGER,
                album_id INTEGER,
                duration INTEGER,
                file_path TEXT UNIQUE NOT NULL,
                cover_path TEXT,
                lyrics TEXT,
                FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE SET NULL,
                FOREIGN KEY (album_id) REFERENCES albums (id) ON DELETE SET NULL
            )
        ''')

        # Создание таблицы плейлистов
        self.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        # Создание таблицы связей между плейлистами и треками
        self.execute('''
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                playlist_id INTEGER,
                track_id INTEGER,
                position INTEGER,
                PRIMARY KEY (playlist_id, track_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
                FOREIGN KEY (track_id) REFERENCES tracks (id) ON DELETE CASCADE
            )
        ''')

    def add_column(self, table: str, column: str, type: str):
        """
        Добавляет новый столбец в указанную таблицу.

        Args:
            table (str): Имя таблицы.
            column (str): Имя нового столбца.
            type (str): Тип данных нового столбца.
        """
        try:
            self.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type}")
        except sqlite3.OperationalError:
            # Столбец может уже существовать, игнорируем ошибку
            pass

    def table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Получает информацию о структуре указанной таблицы.

        Args:
            table_name (str): Имя таблицы.

        Returns:
            List[Dict[str, Any]]: Список словарей с информацией о столбцах таблицы.
        """
        return self.execute(f"PRAGMA table_info({table_name})")

    def ensure_column_exists(self, table: str, column: str, type: str):
        """
        Проверяет наличие столбца в таблице и добавляет его, если он отсутствует.

        Args:
            table (str): Имя таблицы.
            column (str): Имя столбца.
            type (str): Тип данных столбца.
        """
        columns = [col['name'] for col in self.table_info(table)]
        if column not in columns:
            self.add_column(table, column, type)
    
    def backup_database(self) -> str:
        """
        Создает резервную копию текущей базы данных.

        Returns:
            str: Путь к файлу резервной копии.
        """
        backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def delete_database(self):
        """
        Удаляет текущую базу данных.
        """
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def create_new_database(self):
        """
        Создает новую пустую базу данных и инициализирует таблицы.
        """
        self.delete_database()
        self.create_tables()

    def transfer_data(self, old_db_path: str):
        """
        Переносит данные из старой базы данных в новую.

        Args:
            old_db_path (str): Путь к файлу старой базы данных.
        """
        old_db = DatabaseManager(old_db_path)
        
        # Перенос данных для каждой таблицы
        for table in ['artists', 'albums', 'tracks', 'playlists', 'playlist_tracks']:
            old_data = old_db.execute(f"SELECT * FROM {table}")
            if old_data:
                # Получаем информацию о столбцах новой таблицы
                new_columns = [col['name'] for col in self.table_info(table)]
                
                # Фильтруем данные, оставляя только существующие столбцы
                filtered_data = [{k: v for k, v in row.items() if k in new_columns} for row in old_data]
                
                if filtered_data:
                    # Формируем SQL-запрос для вставки данных
                    columns = ', '.join(filtered_data[0].keys())
                    placeholders = ', '.join(['?' for _ in filtered_data[0]])
                    query = f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})"
                    
                    # Вставляем данные
                    for row in filtered_data:
                        self.execute(query, tuple(row.values()))
            
            print(f"Transferred data for table: {table}")

    def migrate_database(self):
        """
        Выполняет миграцию базы данных: создает резервную копию, создает новую базу и переносит данные.
        """
        # Создаем резервную копию
        backup_path = self.backup_database()
        print(f"Backup created at: {backup_path}")

        try:
            # Запоминаем путь к текущей базе
            old_db_path = self.db_path

            # Создаем новую базу данных
            self.create_new_database()
            print("New database created")

            # Переносим данные
            self.transfer_data(old_db_path)
            print("Data transferred to new database")

            # Проверяем, что данные действительно перенесены
            for table in ['artists', 'albums', 'tracks', 'playlists', 'playlist_tracks']:
                count = self.execute(f"SELECT COUNT(*) as count FROM {table}")[0]['count']
                print(f"Table {table} has {count} rows")

            print("Database migration completed successfully")

            # Удаляем бекап после успешной миграции
            os.remove(backup_path)
            print(f"Backup file removed: {backup_path}")

        except Exception as e:
            print(f"Error during migration: {e}")
            print("Restoring from backup...")
            self.delete_database()
            shutil.copy2(backup_path, self.db_path)
            print("Database restored from backup")
            raise
