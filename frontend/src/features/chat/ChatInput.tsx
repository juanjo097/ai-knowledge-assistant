import * as React from "react";
import {
  Box,
  TextField,
  IconButton,
  InputAdornment,
  Tooltip,
  CircularProgress,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

type Props = {
  disabled: boolean;                 
  onSend: (text: string) => void;    
  busy?: boolean;                   
  autoFocus?: boolean;              
};

export default function ChatInput({ disabled, onSend, busy = false, autoFocus }: Props) {
  const [value, setValue] = React.useState("");

  const canSend = !disabled && !busy && value.trim().length > 0;

  const handleSend = React.useCallback(() => {
    const t = value.trim();
    if (!t || disabled || busy) return;
    setValue("");
    onSend(t);
  }, [value, disabled, busy, onSend]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    // Enter -> end | Shift+Enter -> new line | Ctrl/Cmd+Enter -> send

    if (e.key === "Enter" && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      handleSend();
    } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box>
      <TextField
        fullWidth
        multiline
        minRows={1}
        maxRows={6}
        placeholder={
          disabled ? "Upload a file to enable chat" : "Type your question…  (Shift+Enter = newline)"
        }
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        autoFocus={autoFocus}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end" sx={{ alignSelf: "flex-end" }}>
              {busy ? (
                <CircularProgress size={20} />
              ) : (
                <Tooltip title="Send (Enter)">
                  <span>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={handleSend}
                      disabled={!canSend}
                      aria-label="send message"
                    >
                      <SendIcon />
                    </IconButton>
                  </span>
                </Tooltip>
              )}
            </InputAdornment>
          ),
        }}
        sx={{
          "& .MuiOutlinedInput-root": {
            borderRadius: 2,
            alignItems: "flex-end",
          },
        }}
      />
    </Box>
  );
}
