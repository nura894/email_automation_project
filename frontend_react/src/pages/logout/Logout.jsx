import api from "../../api/axios.js"; 
import { useNavigate } from "react-router-dom";

function LogoutButton() {

  const navigate = useNavigate() ;

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token");

      await api.post("/auth/logout", {
        refresh_token: refreshToken
      });

    } catch (err) {
      console.log("Logout error:", err);

    } finally {
      localStorage.clear();
      navigate("/");
    }
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
}

export default LogoutButton;