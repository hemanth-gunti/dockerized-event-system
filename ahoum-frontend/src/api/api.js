import axios from "axios";

const api = axios.create({
  baseURL: "/api/"

});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  // Do NOT attach token for public endpoints
  if (
    token &&
    !config.url.includes("signup") &&
    !config.url.includes("verify-otp") &&
    !config.url.includes("login")
  ) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});


export default api;
