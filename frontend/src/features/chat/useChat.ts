import * as React from "react";
import type { Message } from "../../shared/types";
import { chat, createNote } from "../../shared/api/endpoints";
import { useDoc } from "../../app/DocContext";

export function useChat() {
  const { docId } = useDoc();
  const [messages, setMessages] = React.useState<Message[]>([]);
  const [busy, setBusy] = React.useState(false);

  const send = React.useCallback(
    async (text: string) => {
      if (!docId) throw new Error("Upload a file first");
      const next: Message[] = [...messages, { role: "user", content: text }];
      setMessages(next);
      setBusy(true);
      try {
        const res = await chat(docId, text);
        setMessages([
          ...next,
          { role: "assistant", content: res.answer, sources: res.sources },
        ]);
      } catch (e: unknown) {
        const errorMessage =
          e instanceof Error ? e.message : "An unknown error occurred";
        setMessages([
          ...next,
          { role: "assistant", content: `Error: ${errorMessage}` },
        ]);
      } finally {
        setBusy(false);
      }
    },
    [docId, messages]
  );

  const saveLastAnswer = React.useCallback(
    async (title: string) => {
      const last = [...messages].reverse().find((m) => m.role === "assistant");
      if (!last) throw new Error("No assistant answer to save");
      await createNote(title, last.content);
    },
    [messages]
  );

  return { docId, messages, busy, send, saveLastAnswer };
}
