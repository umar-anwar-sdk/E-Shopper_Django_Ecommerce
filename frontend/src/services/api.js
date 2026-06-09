import axios from "axios";

const api = axios.create({
  baseURL: "https://umaranwar.pythonanywhere.com/api/",
});
// Add token to header 
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");

  if (token) {
    const isJwt = token.split('.').length === 3;
    config.headers.Authorization = isJwt ? `Bearer ${token}` : `Token ${token}`;
  }

  return config;
});
api.interceptors.response.use(
  (response) => response,
  (error) => {
    try {
      const status = error.response?.status;
      if (status === 401) {
        localStorage.removeItem("accessToken");
      
        window.location.href = "/login";
      }
    } catch (e) {
      // ignore
    }
    return Promise.reject(error);
  }
);

export default api;

// import axios from "axios";

// const api = axios.create({
//   baseURL: "https://umaranwar.pythonanywhere.com/api/",
// });
// // Add token to header 
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem("accessToken");

//   if (token) {
//     // If the token looks like a JWT (has two dots), use Bearer scheme
//     const isJwt = token.split('.').length === 3;
//     config.headers.Authorization = isJwt ? `Bearer ${token}` : `Token ${token}`;
//   }

//   return config;
// });



// export default api;
