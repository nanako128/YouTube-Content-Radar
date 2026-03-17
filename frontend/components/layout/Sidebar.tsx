"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  TrendingUp, 
  MessageSquare, 
  Zap, 
  Users, 
  BarChart3 
} from "lucide-react";
import { clsx } from "clsx";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Buzz Rankings", href: "/videos/buzz", icon: TrendingUp },
  { name: "Discussion", href: "/videos/discussion", icon: MessageSquare },
  { name: "Viral Spikes", href: "/videos/viral", icon: Zap },
  { name: "Channels", href: "/channels", icon: Users },
  { name: "Trends", href: "/trends", icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-red-600 flex items-center gap-2">
          <Zap className="fill-red-600" />
          Radar
        </h1>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive 
                  ? "bg-red-50 text-red-600" 
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              )}
            >
              <item.icon className="w-5 h-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-400">© 2026 AI Content Radar</p>
      </div>
    </aside>
  );
}
