import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import api, { setAccessToken } from "./api/axios.js";

import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import UploadCSV  from "./pages/upload_csv/UploadCsv";
import ProtectedRoute from "./api/ProtectedRoute";


function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      try {
        const res = await api.post("/auth/refresh");
        setAccessToken(res.data.access_token);
      } catch {
        console.log("Not logged in");
      } finally {
        setLoading(false);
      }
    };

    init();
  }, []);

  // prevent premature redirect
  if (loading) {
    return ( 
      <div style={styles.container}>
        <div style={styles.spinner}></div>
      </div>
  );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/upload" element={
                        <ProtectedRoute>
                          <UploadCSV />
                        </ProtectedRoute>
                        } />
      </Routes>
    </BrowserRouter>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  spinner: {
    width: "40px",
    height: "40px",
    border: "4px solid #ddd",
    borderTop: "4px solid #3498db",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
};

export default App;