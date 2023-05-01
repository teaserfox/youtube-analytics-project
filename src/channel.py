import os
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        # self.youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = self.__channel['items'][0]['snippet']['title']
        self.__description = self.__channel['items'][0]['snippet']['description']
        self.__url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.__video_title = str(self.__channel['items'][0]['snippet']['title'])
        self.__subscribers_count = int(self.__channel['items'][0]['statistics']['subscriberCount'])
        self.__video_count = int(self.__channel['items'][0]['statistics']['videoCount'])
        self.__views_count = int(self.__channel['items'][0]['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """Геттер возвращает id канала."""
        return self.__channel_id

    # # @channel_id.setter
    #  #def channel_id(self, value):
    #      """Сеттер возвращает id канала."""
    #      print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @property
    def title(self) -> str:
        """Геттер возвращает название канала."""
        return self.__title

    @property
    def description(self) -> str:
        """Геттер возвращает описание канала."""
        return self.__description

    @property
    def url(self) -> str:
        """Геттер возвращает url канала."""
        return self.__url

    @property
    def subscribers_count(self) -> int:
        """Геттер возвращает количество подписчиков канала."""
        return self.__subscribers_count

    @property
    def video_count(self) -> int:
        """Геттер возвращает количество видео канала."""
        return self.__video_count

    @property
    def views_count(self) -> int:
        """Геттер возвращает количество просмотров канала."""
        return self.__views_count

    @classmethod
    def get_service(cls):
        """Класс-метод возвращает объект для работы с YouTube API."""
        return cls.__youtube

    def to_json(self, filename) -> None:
        """Метод возвращает в json значения атрибутов экземпляра Channel."""
        data = {
            'channel_id': self.__channel_id,
            'title': self.__title,
            'description': self.__description,
            'url': self.__url,
            'subscribers_count': self.__subscribers_count,
            'video_count': self.__video_count,
            'views_count': self.__views_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def __str__(self) -> str:
        """
        Отображаем информацию об объектах класса(название канала, ссылка) для пользователей.
        """
        return f'{self.__title} ({self.__url})'

    def __add__(self, other: 'Channel') -> int:
        """
        Метод сложения.
        """
        return self.__subscribers_count + other.__subscribers_count

    def __sub__(self, other: 'Channel') -> int:
        """
        Метод вычитания.
        """
        return self.__subscribers_count - other.__subscribers_count

    def __gt__(self, other: 'Channel') -> bool:
        """
        Метод сравнения больше.
        """
        return self.__subscribers_count > other.__subscribers_count

    def __ge__(self, other: 'Channel') -> bool:
        """
        Метод сравнения больше или равно.
        """
        return self.__subscribers_count >= other.__subscribers_count

    def __lt__(self, other: 'Channel') -> bool:
        """
        Метод сравнения меньше.
        """
        return self.__subscribers_count < other.__subscribers_count

    def __le__(self, other: 'Channel') -> bool:
        """
        Метод сравнения меньше или равно.
        """
        return self.__subscribers_count >= other.__subscribers_count

    def __eq__(self, other: 'Channel') -> bool:
        """
        Метод сравнения равно.
        """
        return self.__subscribers_count == other.__subscribers_count


