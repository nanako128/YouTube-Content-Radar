import { api } from "@/lib/api";
import VideoCard from "@/components/ui/VideoCard";
import { Zap } from "lucide-react";

export default async function ViralRankingsPage() {
  const rankings = await api.getViralSpikes();

  return (
    <div className="space-y-8 pb-12">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-yellow-100 rounded-xl">
          <Zap className="w-8 h-8 text-yellow-600" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Viral Spikes</h1>
          <p className="text-gray-500">Videos whose view velocity exceeds 3× their channel average.</p>
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
          No viral spikes detected recently.
        </div>
      )}
    </div>
  );
}
