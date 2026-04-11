import { Navigate } from "react-router-dom";
import { getAccessToken } from "./axios.js";

const ProtectedRoute = ({ children }) => {
  const token = getAccessToken();

  return token ? children : <Navigate to="/" replace />;
};

export default ProtectedRoute;