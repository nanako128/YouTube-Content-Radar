import { Search, Bell, User } from "lucide-react";

export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
      <div className="flex items-center gap-4 bg-gray-100 px-4 py-2 rounded-full w-96">
        <Search className="w-4 h-4 text-gray-400" />
        <input 
          type="text" 
          placeholder="Search videos, channels, or trends..." 
          className="bg-transparent border-none focus:ring-0 text-sm w-full outline-none"
        />
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 text-gray-400 hover:text-gray-600 relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
        </button>
        <div className="flex items-center gap-3 pl-4 border-l border-gray-200">
          <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
            <User className="w-5 h-5" />
          </div>
          <div className="text-right">
            <p className="text-xs font-semibold">Editor Mode</p>
            <p className="text-[10px] text-gray-400">Content Team</p>
          </div>
        </div>
      </div>
    </header>
  );
}
