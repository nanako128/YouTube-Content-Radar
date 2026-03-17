export interface Video {
  video_id: string;
  title: string;
  publish_time: string;
  view_count: number;
  like_count: number;
  comment_count: number;
  channel_id: string;
  description?: string;
  tags: string[];
}

export interface VideoMetrics {
  buzz_score: number;
  discussion_score?: number;
  view_velocity: number;
  engagement_rate: number;
  fresh_score: number;
  viral_spike: boolean;
}

export interface Ranking {
  rank: number;
  score: number;
  video: Video;
  metrics?: VideoMetrics;
}

export interface Channel {
  channel_id: string;
  name: string;
  subscriber_count?: number;
  is_curated: boolean;
  last_crawled_at?: string;
}
