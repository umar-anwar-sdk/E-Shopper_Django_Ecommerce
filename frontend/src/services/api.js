import axios from "axios";

const api = axios.create({
  baseURL: "https://umaranwar.pythonanywhere.com/api/",
});
// Add token to header 
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");

  if (token) {
    config.headers.Authorization = `Token ${token}`; 
  }

  return config;
});

export default api;