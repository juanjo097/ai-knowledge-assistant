import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import UploadCard from "../features/upload/uploadCard";
import ChatPanel from "../features/chat/ChatPanel";
import { useDoc } from "../app/DocContext";

export default function Home() {
  const { docId } = useDoc();

  return (
    <Box sx={{ py: 2 }}>
      {docId && (
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ mb: 1, display: "block" }}
        >
          Active doc_id: <b>{docId}</b>
        </Typography>
      )}

      <Grid container spacing={2} alignItems="stretch">
        <Grid item xs={12} sm={5} md={4} lg={3} xl={2}>
          <UploadCard />
        </Grid>

        <Grid item xs={12} sm={7} md={8} lg={9} xl={10}>
          <ChatPanel />
        </Grid>
      </Grid>
    </Box>
  );
}
