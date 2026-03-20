import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.config import settings

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str = settings.YOUTUBE_API_KEY):
        self.api_key = api_key

    async def _get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["key"] = self.api_key
        # Accept-Encoding: gzip is handled by httpx automatically
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

    async def get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        params = {
            "part": "contentDetails",
            "id": channel_id,
            "fields": "items/contentDetails/relatedPlaylists/uploads"
        }
        data = await self._get("channels", params)
        if data.get("items"):
            return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        return None

    async def fetch_channel_videos(self, playlist_id: str, published_after: Optional[datetime] = None) -> List[Dict[str, Any]]:
        videos = []
        next_page_token = None
        
        while True:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": 50,
                "fields": "items(snippet(publishedAt,resourceId/videoId,title,description)),nextPageToken"
            }
            if next_page_token:
                params["pageToken"] = next_page_token
            
            data = await self._get("playlistItems", params)
            
            for item in data.get("items", []):
                publish_time_str = item["snippet"]["publishedAt"]
                publish_time = datetime.fromisoformat(publish_time_str.replace("Z", "+00:00"))
                
                if published_after and publish_time < published_after:
                    return videos
                
                videos.append({
                    "video_id": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "publish_time": publish_time,
                })
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
                
        return videos

    async def fetch_video_stats(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        results = []
        # YouTube allows max 50 IDs per request
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            params = {
                "part": "statistics,snippet,contentDetails",
                "id": ",".join(batch),
                "fields": "items(id,statistics(viewCount,likeCount,commentCount),snippet(tags),contentDetails(duration))"
            }
            data = await self._get("videos", params)
            for item in data.get("items", []):
                stats = item.get("statistics", {})
                results.append({
                    "video_id": item["id"],
                    "view_count": int(stats.get("viewCount", 0)),
                    "like_count": int(stats.get("likeCount", 0)),
                    "comment_count": int(stats.get("commentCount", 0)),
                    "tags": item.get("snippet", {}).get("tags", []),
                    "duration": item.get("contentDetails", {}).get("duration"), # ISO 8601 duration
                })
        return results

    async def fetch_video_comments(self, video_id: str, max_results: int = 200) -> List[Dict[str, Any]]:
        comments = []
        next_page_token = None
        
        while len(comments) < max_results:
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": min(100, max_results - len(comments)),
                "textFormat": "plainText",
                "fields": "items(id,snippet/topLevelComment/snippet(textDisplay,likeCount,publishedAt)),nextPageToken"
            }
            if next_page_token:
                params["pageToken"] = next_page_token
            
            try:
                data = await self._get("commentThreads", params)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403: # Comments might be disabled
                    break
                raise
                
            for item in data.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "comment_id": item["id"],
                    "comment_text": snippet["textDisplay"],
                    "like_count": snippet.get("likeCount", 0),
                    "created_at": datetime.fromisoformat(snippet["publishedAt"].replace("Z", "+00:00")),
                })
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
                
        return comments[:max_results]

    async def search_videos(self, query: str, max_results: int = 50, published_after: Optional[datetime] = None) -> List[Dict[str, Any]]:
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": max_results,
            "type": "video",
            "order": "viewCount",
            "fields": "items(id/videoId,snippet(channelId,channelTitle,title,description,publishedAt))"
        }
        if published_after:
            params["publishedAfter"] = published_after.isoformat().replace("+00:00", "Z")
            
        data = await self._get("search", params)
        videos = []
        for item in data.get("items", []):
            videos.append({
                "video_id": item["id"]["videoId"],
                "channel_id": item["snippet"]["channelId"],
                "channel_title": item["snippet"]["channelTitle"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "publish_time": datetime.fromisoformat(item["snippet"]["publishedAt"].replace("Z", "+00:00")),
            })
        return videos

youtube_service = YouTubeService()
