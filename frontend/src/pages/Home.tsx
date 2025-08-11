import Grid from '@mui/material/Grid'
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import UploadCard from '../features/upload/uploadCard'
import ChatPanel from '../features/chat/ChatPanel'

export default function Home() {
  return (
    <Box sx={{ py: 1 }}>
    <Grid container spacing={2} alignItems="stretch">
      <Grid item xs={12} md={4}>
        <Box sx={{ height: "100%", display: "flex", flexDirection: "column", gap: 1.5 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
            1) Upload knowledge file (TXT/CSV)
          </Typography>
          <UploadCard />
        </Box>
      </Grid>

      {/* Columna derecha */}
      <Grid item xs={12} md={8}>
        <Box sx={{ height: "100%", display: "flex", flexDirection: "column", gap: 1.5 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
            2) Chat over your file
          </Typography>
          <ChatPanel />
        </Box>
      </Grid>
    </Grid>
  </Box>
  )
}