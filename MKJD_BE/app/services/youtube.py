from typing import Optional

from googleapiclient.discovery import build


class YouTubeClient:
    def __init__(self, api_key: Optional[str] = None, credentials=None):
        if not api_key and credentials is None:
            raise ValueError("api_key or credentials is required")
        self._client = build(
            "youtube",
            "v3",
            developerKey=api_key,
            credentials=credentials,
            cache_discovery=False,
        )

    def list_comments(
        self,
        video_id: str,
        page_token: Optional[str] = None,
        max_results: int = 100,
    ):
        request = self._client.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="time",
            maxResults=max_results,
            pageToken=page_token,
            textFormat="plainText",
        )
        return request.execute()

    def set_moderation_status(
        self,
        comment_id: str,
        status: str,
        ban_author: bool = False,
    ):
        request = self._client.comments().setModerationStatus(
            id=comment_id,
            moderationStatus=status,
            banAuthor=ban_author,
        )
        return request.execute()

    def list_channels(self, max_results: int = 50):
        request = self._client.channels().list(
            part="snippet,statistics",
            mine=True,
            maxResults=max_results,
        )
        return request.execute()
