import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """
        :id плейлиста
        :название плейлиста
        :ссылка на плейлист
        """
        self.__playlist_id = playlist_id
        self.__playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.__duration = self.youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(self.__playlist_id)
                                                     ).execute()
        self.__video = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.__playlist_id)
                                                         ).execute()
        playlist_videos = self.youtube.playlists().list(part='snippet',
                                                        id=self.__playlist_id,
                                                        ).execute()
        self.title = self.__playlist_videos['items'][0]['snippet']['localized']['title']
        self.url = f'https://www.youtube.com/watch?v={self.__playlist_id}'


    @property
    def total_duration(self):
        res = timedelta()

        for video in self.__video['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            res += duration
        return res

    def show_best_video(self):
        likes = 0

        for video_id in self.__playlist_videos:

            video_request = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            like_count = video_request['items'][0]['statistics']['likeCount']

            if int(like_count) > likes:
                likes = int(like_count)
                best_video = f"https://youtu.be/{video_request['items'][0]['id']}"

        return best_video


