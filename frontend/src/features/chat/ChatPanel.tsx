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
    } catch (e) {
      if (e instanceof Error) {
        setSnack({ open: true, msg: e.message, severity: "error" });
      } else {
        setSnack({ open: true, msg: "An unknown error occurred", severity: "error" });
      }
    }
  }

  return (
    <Card
      variant="outlined"
      sx={{
        height: "70vh",                
        display: "flex",
        flexDirection: "column",
      }}
    >
      <CardHeader
        titleTypographyProps={{ variant: "subtitle1", fontWeight: 700 }}
        title="Chat over your file"
        action={
          <Button
            size="small"
            variant="outlined"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={!messages.some((m) => m.role === "assistant")}
            sx={{ borderRadius: 2 }}
          >
            Save last answer
          </Button>
        }
        sx={{
          position: "sticky",
          top: 0,
          zIndex: 1,
          bgcolor: "background.paper",
          borderBottom: "1px solid",
          borderColor: "divider",
          py: 1.25,
        }}
      />

      {/* Contenido en columna: mensajes (scrollea) + input (fijo abajo) */}
      <CardContent
        sx={{
          p: 0,
          flex: 1,                  
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",      
        }}
      >
        {/* Área de mensajes que sí scrollea */}
        <Box
          ref={scrollerRef}
          sx={{
            flex: "1 1 0",
            minHeight: 0,           
            overflowY: "auto",
            px: 2,
            py: 1.5,
          }}
        >
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

        {/* ChatInput here */}
        <Box
          sx={{
            borderTop: "1px solid",
            borderColor: "divider",
            bgcolor: "background.paper",
            p: 1.25,
          }}
        >
          <ChatInput disabled={!docId || busy} onSend={send} />
        </Box>
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
