import * as React from "react";
import { Paper, TextField, Button, Stack } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

export default function ChatInput({
  disabled,
  onSend,
}: {
  disabled: boolean;
  onSend: (text: string) => void;
}) {
  const [value, setValue] = React.useState("");
  async function handle() {
    const t = value.trim();
    if (!t) return;
    setValue("");
    onSend(t);
  }
  return (
    <Paper
      elevation={2}
      sx={{ p: 1, position: "sticky", bottom: 0, bgcolor: "background.paper" }}
    >
      <Stack direction="row" spacing={1}>
        <TextField
          fullWidth
          size="small"
          placeholder={
            disabled ? "Upload a file to enable chat" : "Type your question…"
          }
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => (e.key === "Enter" ? handle() : undefined)}
          disabled={disabled}
        />
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          onClick={handle}
          disabled={disabled}
        >
          Send
        </Button>
      </Stack>
    </Paper>
  );
}
