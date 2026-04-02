import { useState } from "react";
import LogoutButton from "../logout/Logout.jsx";
import api from "../../api/axios.js";

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post(
        "http://localhost:8000/upload_csv/upload-csv/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",

          },
        }
      );

      setMessage(` Success: ${res.data.total} processed, ${res.data.failed} failed`);
    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2>Upload CSV</h2>

        <form onSubmit={handleUpload}>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button type="submit">Submit</button>
        </form>

        <p>{message}</p>
        <LogoutButton/>
        
      </div>
    </div>
  );
}

const styles = {

  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#779eda",
  },
  card: {
    padding: "2rem",
    background: "#ffffff",
    borderRadius: "10px",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
    textAlign: "center",
  },


};

export default UploadCSV;