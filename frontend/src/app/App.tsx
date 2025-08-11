import { Container, Box } from "@mui/material";
import { AppTheme } from "../shared/theme";
import { DocProvider } from "./DocContext";
import AppHeader from "./AppHeader";
import { BrowserRouter, Routes, Route, Outlet, Navigate } from "react-router-dom";
import ProtectedRoute from "../shared/router/ProtectedRoute";

import Home from "../pages/Home";
import LoginPage from "../features/auth/LoginPage"
import ChatPage from "../features/chat/ChatPanel";
import NotesList from "../features/notes/NotesList";

function Shell() {
  return (
    <>
      <AppHeader />
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Outlet />
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
        <BrowserRouter>
          <Routes>
            {/* Public */}
            <Route path="/login" element={<LoginPage />} />

            {/* Protected */}
            <Route element={<ProtectedRoute />}>
              <Route element={<Shell />}>
                <Route path="/" element={<Home />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/notes" element={<NotesList />} />
              </Route>
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </DocProvider>
    </AppTheme>
  );
}
