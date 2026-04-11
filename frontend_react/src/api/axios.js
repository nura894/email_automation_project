import axios from "axios";


let accessToken =null;

export const setAccessToken = (token) =>{
  accessToken = token;
}

export const getAccessToken =() => accessToken;


const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});



api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (originalRequest?.url?.includes("/auth/refresh")) {
      return Promise.reject(error);
    }

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const res = await api.post('/auth/refresh');
        
        const newToken = res.data.access_token;
        setAccessToken(newToken);

        originalRequest.headers.Authorization = `Bearer ${newToken}`;

        return api(originalRequest);

      } catch (err) {
        console.log(err);
        setAccessToken(null);
        // window.location.href = "/"; //login_page

        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default api;