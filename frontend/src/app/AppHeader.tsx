import { AppBar, Toolbar, Tabs, Tab, Box } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import LogoutIcon from "@mui/icons-material/Logout";
import IconButton from "@mui/material/IconButton";
import { clearToken } from "../features/auth/auth";

const routes = ["/", "/chat", "/notes"];

export default function AppHeader() {
  const { pathname } = useLocation();
  const nav = useNavigate();
  const value = routes.includes(pathname) ? routes.indexOf(pathname) : 0;

  return (
    <AppBar position="static" elevation={0}>
      <Toolbar sx={{ gap: 2 }}>
        <Box sx={{ fontWeight: 800, letterSpacing: 0.4 }}>
          AI Knowledge Assistant
        </Box>
        <Tabs
          value={value}
          onChange={(_, v) => nav(routes[v])}
          textColor="inherit"
          indicatorColor="secondary"
        >
          <Tab label="Home" />
          <Tab label="Chat" />
          <Tab label="Notes" />
        </Tabs>
        <Box sx={{ flex: 1 }} />
        <IconButton
          color="inherit"
          onClick={() => {
            clearToken();
            nav("/login");
          }}
          aria-label="logout"
        >
          <LogoutIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}
