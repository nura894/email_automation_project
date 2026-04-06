import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios  from "axios";

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(()=>{
    const verifyUser = async ()=>{
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        setIsAuthenticated(false);
        return ;
      }

      try{
        await axios.get("http://localhost:8000/auth/protected", 
          {headers : {Authorization : `Bearer ${accessToken}`,},}
        );
        setIsAuthenticated(true);
      }catch {
        setIsAuthenticated(false);
      }

    };
    verifyUser();
  },[]);
  
  if (isAuthenticated === null) {
      return <div>Loading...</div>;
    }

  return isAuthenticated ? children : <Navigate to= '/' replace/>;
  
};

export default ProtectedRoute;