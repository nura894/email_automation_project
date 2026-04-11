import {  Navigate } from "react-router-dom";
import { useEffect, useState } from "react";



const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(()=>{
    const verifyUser = async ()=>{
      let accessToken = localStorage.getItem("access_token");
      
      if (!accessToken){
        setIsAuthenticated(false);
        return
      }
        setIsAuthenticated(true)
      };

    verifyUser();
  },[]);
  
  if (isAuthenticated === null) {
  return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to= '/' replace/>;
  
};

export default ProtectedRoute;