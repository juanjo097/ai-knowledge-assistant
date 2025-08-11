import * as React from "react";

interface DocState {
  docId: number | null;
  setDocId: (id: number | null) => void;
}
const Ctx = React.createContext<DocState | null>(null);

export function DocProvider({ children }: { children: React.ReactNode }) {
  const [docId, setDocId] = React.useState<number | null>(null);
  const value = React.useMemo(() => ({ docId, setDocId }), [docId]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useDoc() {
  const ctx = React.useContext(Ctx);
  if (!ctx) throw new Error("useDoc must be used within DocProvider");
  return ctx;
}
