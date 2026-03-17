import { api } from "@/lib/api";
import VideoCard from "@/components/ui/VideoCard";
import { TrendingUp } from "lucide-react";

export default async function BuzzRankingsPage() {
  const rankings = await api.getTopBuzz();

  return (
    <div className="space-y-8 pb-12">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-red-100 rounded-xl">
          <TrendingUp className="w-8 h-8 text-red-600" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Top Buzz Rankings</h1>
          <p className="text-gray-500">Trending videos based on views, engagement, and freshness.</p>
        </div>
      </div>

      {rankings.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {rankings.map((ranking) => (
            <VideoCard key={ranking.video.video_id} ranking={ranking} />
          ))}
        </div>
      ) : (
        <div className="h-96 border-2 border-dashed border-gray-200 rounded-2xl flex items-center justify-center text-gray-400">
          No buzz rankings found.
        </div>
      )}
    </div>
  );
}
