import os
from googleapiclient.discovery import build


class Mixin_id:

    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self) -> None:
        self.api_key = self.__api_key
        self.youtube = self.__youtube

    @classmethod
    def get_service(cls):
        """Класс-метод возвращает объект для работы с YouTube API."""
        return cls.__youtube