import * as React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  Snackbar,
  Alert,
  Box,
  Button,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";
import MessageBubble from "./MessageBubble";
import { useChat } from "./useChat";
import ChatInput from "./ChatInput";

export default function ChatPanel() {
  const { docId, messages, busy, send, saveLastAnswer } = useChat();
  const [snack, setSnack] = React.useState<{
    open: boolean;
    msg: string;
    severity: "success" | "error";
  }>({ open: false, msg: "", severity: "success" });
  const scrollerRef = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    scrollerRef.current?.scrollTo({ top: scrollerRef.current.scrollHeight });
  }, [messages]);

  async function handleSave() {
    const title = prompt("Note title:", "Chat answer") || "Chat answer";
    try {
      await saveLastAnswer(title);
      setSnack({ open: true, msg: "Note saved", severity: "success" });
    } catch (e: any) {
      setSnack({ open: true, msg: e.message, severity: "error" });
    }
  }

  return (
    <Card
      variant="outlined"
      sx={{ height: "70vh", display: "flex", flexDirection: "column" }}
    >
      <CardHeader
        title="2) Chat over your file"
        action={
          <Button
            size="small"
            variant="contained"
            color="secondary"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={!messages.some((m) => m.role === "assistant")}
          >
            Save last answer
          </Button>
        }
      />
      <CardContent
        sx={{
          pt: 0,
          display: "flex",
          flexDirection: "column",
          height: "100%",
          gap: 1,
        }}
      >
        <Box ref={scrollerRef} sx={{ flex: 1, overflow: "auto", p: 1 }}>
          {messages.length === 0 ? (
            <Box
              sx={{
                color: "text.secondary",
                fontSize: 14,
                height: "100%",
                display: "grid",
                placeItems: "center",
              }}
            >
              Ask something that exists in the uploaded document.
            </Box>
          ) : (
            messages.map((m, i) => <MessageBubble key={i} m={m} />)
          )}
        </Box>
        <ChatInput disabled={!docId || busy} onSend={send} />
      </CardContent>
      <Snackbar
        open={snack.open}
        autoHideDuration={2500}
        onClose={() => setSnack((s) => ({ ...s, open: false }))}
      >
        <Alert
          severity={snack.severity}
          onClose={() => setSnack((s) => ({ ...s, open: false }))}
        >
          {snack.msg}
        </Alert>
      </Snackbar>
    </Card>
  );
}
