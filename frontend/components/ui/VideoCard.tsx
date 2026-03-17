import { Ranking } from "@/types";
import { formatDistanceToNow } from "date-fns";
import { Eye, ThumbsUp, MessageSquare, ExternalLink } from "lucide-react";

interface VideoCardProps {
  ranking: Ranking;
  showScore?: boolean;
}

export default function VideoCard({ ranking, showScore = true }: VideoCardProps) {
  const { video, metrics, rank, score } = ranking;
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      <div className="relative aspect-video bg-gray-100">
        <img 
          src={`https://img.youtube.com/vi/${video.video_id}/mqdefault.jpg`} 
          alt={video.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute top-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-xs font-bold">
          #{rank}
        </div>
        {showScore && (
          <div className="absolute bottom-2 right-2 bg-red-600 text-white px-2 py-1 rounded text-sm font-bold flex items-center gap-1">
            {score.toFixed(1)}
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 line-clamp-2 h-10 mb-2 leading-tight">
          {video.title}
        </h3>
        <p className="text-xs text-gray-500 mb-3">
          {formatDistanceToNow(new Date(video.publish_time), { addSuffix: true })}
        </p>
        
        <div className="flex items-center justify-between mt-4 text-[10px] text-gray-400 font-medium">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              {(video.view_count / 1000).toFixed(1)}K
            </span>
            <span className="flex items-center gap-1">
              <ThumbsUp className="w-3 h-3" />
              {(video.like_count / 1000).toFixed(1)}K
            </span>
            <span className="flex items-center gap-1">
              <MessageSquare className="w-3 h-3" />
              {video.comment_count}
            </span>
          </div>
          <a 
            href={`https://youtube.com/watch?v=${video.video_id}`} 
            target="_blank" 
            className="text-red-600 hover:text-red-700 flex items-center gap-1"
          >
            Watch <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}
