import { api } from "@/lib/api";
import { Users, Globe, CheckCircle, AlertCircle } from "lucide-react";

export default async function ChannelsPage() {
  let channels = [];
  let error = null;

  try {
    channels = await api.getChannels();
  } catch (e) {
    console.error("Failed to fetch channels:", e);
    error = "Unable to connect to the API. Please ensure the backend server is running.";
  }

  return (
    <div className="space-y-8 pb-12">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-purple-100 rounded-xl">
          <Globe className="w-8 h-8 text-purple-600" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tracked Channels</h1>
          <p className="text-gray-500">Curated list of channels being monitored for content radar.</p>
        </div>
      </div>

      {error ? (
        <div className="p-6 bg-amber-50 border border-amber-200 rounded-2xl flex items-center gap-3 text-amber-800">
          <AlertCircle className="w-5 h-5" />
          <p>{error}</p>
        </div>
      ) : channels.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {channels.map((channel) => (
            <div key={channel.channel_id} className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center font-bold text-gray-400">
                    {channel.name.charAt(0)}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 flex items-center gap-1">
                      {channel.name}
                      {channel.is_curated && <CheckCircle className="w-4 h-4 text-blue-500" />}
                    </h3>
                    <p className="text-sm text-gray-500">ID: {channel.channel_id}</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 pt-6 border-t border-gray-50 flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 text-gray-600">
                  <Users className="w-4 h-4" />
                  <span>{channel.subscriber_count?.toLocaleString() || "N/A"} subs</span>
                </div>
                <div className="text-gray-400">
                  Last crawled: {channel.last_crawled_at ? new Date(channel.last_crawled_at).toLocaleDateString() : "Never"}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="h-64 border-2 border-dashed border-gray-200 rounded-xl flex items-center justify-center text-gray-400">
          No channels tracked yet.
        </div>
      )}
    </div>
  );
}
