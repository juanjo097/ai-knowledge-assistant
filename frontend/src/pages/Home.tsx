import Grid from '@mui/material/Grid'
import UploadCard from '../features/upload/uploadCard'
import ChatPanel from '../features/chat/ChatPanel'

export default function Home() {
  return (
    <Grid container spacing={2}>
      <Grid xs={12} md={4}>
        <UploadCard />
      </Grid>
      <Grid xs={12} md={8}>
        <ChatPanel />
      </Grid>
    </Grid>
  )
}