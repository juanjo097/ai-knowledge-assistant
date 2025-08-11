import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  InputAdornment,
  IconButton,
} from "@mui/material";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import { http } from "../../shared/api/http";
import { saveToken } from "./auth";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [username, setU] = useState("");
  const [password, setP] = useState("");
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await http.post<{ token: string }>("/auth/login", {
        username,
        password,
      });
      saveToken(data.token);
      nav("/", { replace: true });
    } catch (err: any) {
      setError(err?.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        px: 2,
        py: 4,
        bgcolor: (t) => t.palette.background.default,
      }}
    >
      <Paper
        elevation={1}
        sx={{
          width: "100%",
          maxWidth: 420,
          borderRadius: 3,
          p: 4,
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        {/* Encabezado simple */}
        <Box>
          <Typography variant="h5" fontWeight={800}>
            Sign in
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Login to continue.
          </Typography>
        </Box>

        <Box component="form" onSubmit={onSubmit} noValidate>
          <TextField
            label="Username"
            fullWidth
            margin="normal"
            value={username}
            onChange={(e) => setU(e.target.value)}
            autoComplete="username"
          />

          <TextField
            label="Password"
            type={showPwd ? "text" : "password"}
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setP(e.target.value)}
            autoComplete="current-password"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowPwd((s) => !s)}
                    edge="end"
                  >
                    {showPwd ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          {error && (
            <Alert severity="error" sx={{ mt: 1 }}>
              {error}
            </Alert>
          )}

          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ mt: 2, py: 1.2, borderRadius: 2, fontWeight: 700 }}
            disabled={!username || !password || loading}
          >
            {loading ? "Signing in..." : "Login"}
          </Button>
        </Box>

        {/* Pie de página discreto */}
        <Typography variant="caption" color="text.secondary" textAlign="center">
        Tip: credentials are defined in the backend (.env)
        </Typography>
      </Paper>
    </Box>
  );
}
