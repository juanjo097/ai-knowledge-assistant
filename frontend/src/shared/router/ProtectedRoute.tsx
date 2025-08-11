import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "../../features/auth/auth";

export default function ProtectedRoute() {
  return isAuthenticated() ? <Outlet /> : <Navigate to="/login" replace />;
}
