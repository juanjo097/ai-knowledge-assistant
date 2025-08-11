import { Container, Box, Stack, Typography } from "@mui/material";
import { AppTheme } from "../shared/theme";
import { DocProvider, useDoc } from "./DocContext";
import Home from "../pages/Home";
import AppHeader from "./AppHeader";

function Shell() {
  const { docId } = useDoc();
  return (
    <>
      <AppHeader />
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <Stack spacing={1} mb={1}>
          <Typography variant="body2" color="text.secondary">
            Upload a file → ask grounded questions → optionally save answers as
            notes.
          </Typography>
          {docId && (
            <Typography variant="caption" color="text.secondary">
              Active doc_id: <b>{docId}</b>
            </Typography>
          )}
        </Stack>
        <Home />
        <Box mt={4} textAlign="center" color="text.secondary" fontSize={12}>
          MVP • RAG + Notes Tool
        </Box>
      </Container>
    </>
  );
}

export default function App() {
  return (
    <AppTheme>
      <DocProvider>
        <Shell />
      </DocProvider>
    </AppTheme>
  );
}
