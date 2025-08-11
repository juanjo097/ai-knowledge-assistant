import * as React from 'react'
import { Card, CardContent, CardHeader, Button, Stack, Typography, LinearProgress } from '@mui/material'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import { useUpload } from './useUpload'

export default function UploadCard() {
  const inputRef = React.useRef<HTMLInputElement | null>(null)
  const { busy, error, fileName, onFile } = useUpload()

  return (
    <Card variant="outlined">
      <CardHeader title="1) Upload knowledge file (TXT/CSV)" />
      {busy && <LinearProgress />}
      <CardContent>
        <Stack direction="row" spacing={2} alignItems="center">
          <input
            ref={inputRef}
            type="file"
            accept=".txt,.csv"
            style={{ display: 'none' }}
            onChange={e => {
              const f = e.target.files?.[0]; if (f) onFile(f)
            }}
          />
          <Button variant="contained" startIcon={<UploadFileIcon />} onClick={() => inputRef.current?.click()} disabled={busy}>
            {busy ? 'Processing…' : 'Choose file'}
          </Button>
          {fileName && (
            <Typography variant="body2" color="text.secondary">Last uploaded: <b>{fileName}</b></Typography>
          )}
        </Stack>
        {error && <Typography mt={1} color="error" variant="body2">{error}</Typography>}
        <Typography mt={1} variant="caption" color="text.secondary">We will normalize, chunk, embed and index on the backend.</Typography>
      </CardContent>
    </Card>
  )
}