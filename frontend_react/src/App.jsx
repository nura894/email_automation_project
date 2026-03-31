import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import UploadCSV  from "./pages/upload_csv/UploadCsv";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/upload" element={<UploadCSV />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;