import { BarChart3 } from "lucide-react";

export default function TrendsPage() {
  return (
    <div className="space-y-8 pb-12">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-indigo-100 rounded-xl">
          <BarChart3 className="w-8 h-8 text-indigo-600" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Trends & Topics</h1>
          <p className="text-gray-500">Topic clusters and emerging trends across monitored channels.</p>
        </div>
      </div>

      <div className="h-96 border-2 border-dashed border-gray-200 rounded-2xl flex flex-col items-center justify-center text-gray-400 gap-4">
        <div className="p-4 bg-gray-50 rounded-full">
          <BarChart3 className="w-12 h-12" />
        </div>
        <div className="text-center">
          <h3 className="text-xl font-bold text-gray-600">Phase 2: AI Trend Detection</h3>
          <p className="max-w-md mt-2">
            This feature is part of the Phase 2 roadmap. It will use HDBSCAN topic clustering 
            and sentence-transformers to automatically group videos into emerging topics.
          </p>
        </div>
      </div>
    </div>
  );
}
