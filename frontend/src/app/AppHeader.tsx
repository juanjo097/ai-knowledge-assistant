import { AppBar, Toolbar, Typography, Box } from "@mui/material";

export default function AppHeader() {
  return (
    <AppBar
      position="sticky"
      elevation={0}
      color="transparent"
      sx={{ backdropFilter: "blur(6px)" }}
    >
      <Toolbar sx={{ minHeight: 72 }}>
        <Typography variant="h6" fontWeight={800}>
          AI Knowledge Assistant
        </Typography>
        <Box sx={{ flex: 1 }} />
        {/* Placeholder for future actions (theme toggle, links, etc.) */}
      </Toolbar>
    </AppBar>
  );
}
