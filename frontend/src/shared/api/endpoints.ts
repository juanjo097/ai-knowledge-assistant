import { http } from "./http";
import type { IngestResponse, ChatResponse, Note } from "../types";

export function pipelineIngest(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  return http.postForm<IngestResponse>(`/pipeline/ingest`, fd);
}

export function chat(doc_id: number, message: string) {
  return http.post<ChatResponse>(`/chat`, { doc_id, message });
}

export function createNote(title: string, content: string) {
  return http.post<Pick<Note, "id" | "title">>(`/tools/create_note`, {
    title,
    content,
  });
}

export function listNotes() {
  return http.get<Note[]>(`/tools/notes`);
}
