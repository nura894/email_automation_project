import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("refresh_token");

  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

export default ProtectedRoute;