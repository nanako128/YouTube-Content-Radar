import { Ranking, Channel } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    cache: "no-store", // For real-time daily rankings
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  getTopBuzz: () => fetchAPI<Ranking[]>("/videos/top-buzz"),
  getTopDiscussion: () => fetchAPI<Ranking[]>("/videos/top-discussion"),
  getViralSpikes: () => fetchAPI<Ranking[]>("/videos/viral"),
  getChannels: () => fetchAPI<Channel[]>("/channels"),
};
