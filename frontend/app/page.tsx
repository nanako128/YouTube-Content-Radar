import { api } from "@/lib/api";
import VideoCard from "@/components/ui/VideoCard";
import { TrendingUp, MessageSquare, Zap, ChevronRight } from "lucide-react";
import Link from "next/link";

export default async function Home() {
  // Use try-catch or handle empty states since API might not be running
  let buzzRankings = [];
  let discussionRankings = [];
  let viralRankings = [];

  try {
    [buzzRankings, discussionRankings, viralRankings] = await Promise.all([
      api.getTopBuzz(),
      api.getTopDiscussion(),
      api.getViralSpikes(),
    ]);
  } catch (error) {
    console.error("Failed to fetch rankings:", error);
  }

  return (
    <div className="space-y-12 pb-12">
      <section>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Top Buzz</h2>
              <p className="text-sm text-gray-500">Highest engagement and view potential</p>
            </div>
          </div>
          <Link href="/videos/buzz" className="text-red-600 hover:text-red-700 font-semibold text-sm flex items-center gap-1">
            View All <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
        
        {buzzRankings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {buzzRankings.slice(0, 4).map((ranking) => (
              <VideoCard key={ranking.video.video_id} ranking={ranking} />
            ))}
          </div>
        ) : (
          <div className="h-64 border-2 border-dashed border-gray-200 rounded-xl flex items-center justify-center text-gray-400">
            No rankings available today. Start a crawl to generate data.
          </div>
        )}
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <MessageSquare className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Discussion Leaders</h2>
              <p className="text-sm text-gray-500">Videos sparking high debate and sentiment conflict</p>
            </div>
          </div>
          <Link href="/videos/discussion" className="text-blue-600 hover:text-blue-700 font-semibold text-sm flex items-center gap-1">
            View All <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        {discussionRankings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {discussionRankings.slice(0, 4).map((ranking) => (
              <VideoCard key={ranking.video.video_id} ranking={ranking} />
            ))}
          </div>
        ) : (
          <div className="h-64 border-2 border-dashed border-gray-200 rounded-xl flex items-center justify-center text-gray-400">
            No discussion rankings available.
          </div>
        )}
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Zap className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Viral Spikes</h2>
              <p className="text-sm text-gray-500">Velocity exceeding 3x channel average</p>
            </div>
          </div>
          <Link href="/videos/viral" className="text-yellow-600 hover:text-yellow-700 font-semibold text-sm flex items-center gap-1">
            View All <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        {viralRankings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {viralRankings.slice(0, 4).map((ranking) => (
              <VideoCard key={ranking.video.video_id} ranking={ranking} />
            ))}
          </div>
        ) : (
          <div className="h-64 border-2 border-dashed border-gray-200 rounded-xl flex items-center justify-center text-gray-400">
            No viral spikes detected.
          </div>
        )}
      </section>
    </div>
  );
}
