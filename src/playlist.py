import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build
from src.mixin_id import Mixin_id


class PlayList(Mixin_id):

    # api_key: str = os.getenv('YT_API_KEY')
    # youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        super().__init__()
        self.__playlist_id = playlist_id
        self.__playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                                   maxResults=50, ).execute()
        self.__video_ids = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]

        self.__video = self.youtube.videos().list(part='contentDetails,statistics',
                                                  id=','.join(self.__video_ids)).execute()
        self.__playlist_info = self.youtube.playlists().list(part='snippet',
                                                             id=self.__playlist_id, ).execute()
        self.title = self.__playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @property
    def total_duration(self):
        total = timedelta(seconds=0)
        for video in self.__video['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        best_video = ""
        likes = 0
        for video in self.__video["items"]:
            like_count = video['statistics']['likeCount']
            if int(like_count) > likes:
                likes = int(like_count)
                best_video = f"https://youtu.be/{video['id']}"
        return best_video
