import * as React from "react";
import type { Message } from "../../shared/types";
import {
  Paper,
  Chip,
  Stack,
  Typography,
  Avatar,
  IconButton,
  Collapse,
} from "@mui/material";
import SourceIcon from "@mui/icons-material/Source";

export default function MessageBubble({ m }: { m: Message }) {
  const isUser = m.role === "user";
  const [open, setOpen] = React.useState(false);

  return (
    <Stack
      direction="row"
      justifyContent={isUser ? "flex-end" : "flex-start"}
      my={1}
      spacing={1}
    >
      {!isUser && <Avatar sx={{ bgcolor: "primary.main" }}>A</Avatar>}
      <Paper
        elevation={1}
        sx={{
          px: 2,
          py: 1.5,
          maxWidth: "75%",
          bgcolor: isUser ? "primary.main" : "background.default",
          color: isUser ? "primary.contrastText" : "text.primary",
        }}
      >
        <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
          {m.content}
        </Typography>
        {!isUser && m.sources && m.sources.length > 0 && (
          <>
            <IconButton
              size="small"
              onClick={() => setOpen((v) => !v)}
              sx={{ mt: 0.5 }}
              aria-label="toggle sources"
            >
              <SourceIcon fontSize="small" />
            </IconButton>
            <Collapse in={open}>
              <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
                {m.sources.map((s, i) => (
                  <Chip
                    key={i}
                    size="small"
                    label={`chunk ${s.chunk_id} (${s.score.toFixed(2)})`}
                  />
                ))}
              </Stack>
            </Collapse>
          </>
        )}
      </Paper>
      {isUser && (
        <Avatar sx={{ bgcolor: "grey.300", color: "text.primary" }}>U</Avatar>
      )}
    </Stack>
  );
}
