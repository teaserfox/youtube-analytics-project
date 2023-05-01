import os
from googleapiclient.discovery import build


class Video:
    """
    Родительский класс видео.
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video: str) -> None:
        """
        Экземпляр инициализируется id канала video.id видео
        :название видео
        :ссылка на видео
        :количество просмотров
        :количество лайков
        """
        self.__id_video = id_video
        self.__video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                  id=self.__id_video).execute()
        self.__title = self.__video['items'][0]['snippet']['title']
        self.__url = f'https://www.youtube.com/watch?v={self.__id_video}'
        self.__view_count = self.__video['items'][0]['statistics']['viewCount']
        self.__like_count = self.__video['items'][0]['statistics']['likeCount']

    @property
    def title(self) -> str:
        """
        Геттер возвращает название видео.
        """
        return self.__title

    @property
    def url(self) -> str:
        """
       Геттер возвращает ссылку на видео.
       """
        return self.__url

    @property
    def view_count(self) -> int:
        """
       Геттер возвращает количество просмотров.
       """
        return self.__view_count

    @property
    def like_count(self) -> int:
        """
       Геттер возвращает количество лайков.
       """
        return self.__like_count

    def __str__(self):
        return self.__title


class PLVideo(Video):
    """
    Дочерний класс от video.
    + свой параметр playlist.
    """

    def __init__(self, id_video, playlist_id) -> None:
        super().__init__(
            id_video)  # возвращает ссылку на объект-посредник, через который происходит вызов методов базового класса
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
