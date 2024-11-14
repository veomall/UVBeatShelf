# Документация модуля MusicLibrary
## Описание
Модуль MusicLibrary представляет собой центральный интерфейс для управления музыкальной библиотекой. Он объединяет функциональность работы с треками, плейлистами, альбомами и исполнителями, используя базу данных SQLite для хранения информации.

## Установка
Для использования модуля MusicLibrary, убедитесь, что у вас установлены все необходимые зависимости. Модуль использует стандартную библиотеку Python и SQLite, поэтому дополнительная установка обычно не требуется.

## Использование
### Инициализация библиотеки
```python
from models.music_library import MusicLibrary

# Инициализация музыкальной библиотеки
db_path = "path/to/your/database.sqlite"
media_root = "path/to/your/media/files"
library = MusicLibrary(db_path, media_root)
```
### Работа с треками
```python
# Добавление нового трека
track_id = library.add_track("My Song", "path/to/song.mp3", artist_id=1, album_id=1)

# Получение информации о треке
track_info = library.get_track_info(track_id)
print(track_info)

# Обновление информации о треке
library.update_track(track_id, title="New Title")

# Удаление трека
library.delete_track(track_id)
```
### Работа с плейлистами
```python
# Создание нового плейлиста
playlist_id = library.create_playlist("My Playlist")

# Добавление трека в плейлист
library.add_track_to_playlist(playlist_id, track_id)

# Получение треков плейлиста
playlist_tracks = library.get_playlist_tracks(playlist_id)
print(playlist_tracks)

# Изменение позиции трека в плейлисте
library.change_track_position_in_playlist(playlist_id, track_id, new_position=2)

# Удаление плейлиста
library.delete_playlist(playlist_id)
```
### Работа с исполнителями
```python
# Добавление нового исполнителя
artist_id = library.add_artist("Artist Name")

# Получение информации об исполнителе
artist_info = library.get_artist_info(artist_id)
print(artist_info)

# Получение альбомов исполнителя
artist_albums = library.get_artist_albums(artist_id)
print(artist_albums)

# Удаление исполнителя
library.delete_artist(artist_id)
```
### Работа с альбомами
```python
# Добавление нового альбома
album_id = library.add_album("Album Title", artist_id, year=2023)

# Получение информации об альбоме
album_info = library.get_album_info(album_id)
print(album_info)

# Добавление трека в альбом
library.add_track_to_album(album_id, track_id, track_number=1)

# Получение треков альбома
album_tracks = library.get_album_tracks(album_id)
print(album_tracks)

# Удаление альбома
library.delete_album(album_id)
```
### Обновление базы данных
```python
# Выполнение миграции базы данных
library.update_db()
```
## Примечания
Все методы, возвращающие ID (например, `add_track`, `create_playlist`), возвращают целочисленный идентификатор созданного или обновленного объекта.
Методы, получающие информацию (например, `get_track_info`, `get_playlist_info`), возвращают словарь с данными объекта.
Методы удаления (например, `delete_track`, `delete_playlist`) возвращают количество удаленных записей.


## Обработка ошибок
Модуль использует встроенную обработку ошибок SQLite. В случае возникновения ошибок при выполнении запросов, они будут выведены в консоль. Рекомендуется обрабатывать возможные исключения при использовании методов модуля.
```python
try:
    track_id = library.add_track("My Song", "path/to/song.mp3")
except Exception as e:
    print(f"Error adding track: {e}")
```
