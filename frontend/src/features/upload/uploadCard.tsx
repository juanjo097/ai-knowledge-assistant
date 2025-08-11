import * as React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  Button,
  Stack,
  Typography,
  LinearProgress,
  Box,
} from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { useUpload } from "./useUpload";

const ACCEPT = ".txt,.csv";

export default function UploadCard() {
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const { busy, error, fileName, onFile } = useUpload();

  const [dragOver, setDragOver] = React.useState(false);

  function handlePick() {
    if (!busy) inputRef.current?.click();
  }

  function handleSelect(f?: File) {
    if (f && !busy) onFile(f);
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const f = e.dataTransfer.files?.[0];
    handleSelect(f);
  }

  return (
    <Card
      variant="outlined"
      sx={{ borderRadius: 3, overflow: "hidden" }}
      aria-busy={busy ? "true" : "false"}
    >
      <CardHeader
        titleTypographyProps={{ variant: "subtitle1", fontWeight: 700 }}
        title="Upload knowledge file (TXT/CSV)"
        sx={{ pb: 0.5 }}
      />

      {busy && <LinearProgress />}

      <CardContent sx={{ pt: 1.5 }}>
        {/* Hiddern Input */}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPT}
          style={{ display: "none" }}
          onChange={(e) => handleSelect(e.target.files?.[0] || undefined)}
        />

        {/* Dropzone */}
        <Box
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={handlePick}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && handlePick()}
          sx={{
            borderRadius: 2,
            border: "1px dashed",
            borderColor: dragOver ? "primary.main" : "divider",
            bgcolor: dragOver ? "action.hover" : "background.paper",
            transition: "all .15s ease",
            p: 2,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 2,
            cursor: busy ? "not-allowed" : "pointer",
            opacity: busy ? 0.6 : 1,
          }}
        >
          <Stack spacing={0.5}>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {fileName ? "Last uploaded:" : "Drag & drop your file here"}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 360 }} noWrap>
              {fileName ? <b title={fileName}>{fileName}</b> : "or click to browse — accepted: TXT, CSV"}
            </Typography>
          </Stack>

          <Button
            variant="contained"
            startIcon={<UploadFileIcon />}
            onClick={(e) => {
              e.stopPropagation();
              handlePick();
            }}
            disabled={busy}
            sx={{ borderRadius: 2, px: 2.5 }}
          >
            {busy ? "Processing…" : fileName ? "Replace file" : "Choose file"}
          </Button>
        </Box>

        {/* Messages */}
        {error ? (
          <Typography mt={1.5} color="error" variant="body2">
            {error}
          </Typography>
        ) : (
          <Typography mt={1.5} variant="caption" color="text.secondary">
            We will normalize, chunk, embed and index on the backend.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
