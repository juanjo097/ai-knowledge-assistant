export type Role = "user" | "assistant";
export interface ChatSource {
  chunk_id: number;
  score: number;
}
export interface Message {
  role: Role;
  content: string;
  sources?: ChatSource[];
}

// API response types
export interface IngestResponse {
  doc_id: number;
  [k: string]: unknown;
}
export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}
export interface Note {
  id: number;
  title: string;
  created_at?: string;
}
