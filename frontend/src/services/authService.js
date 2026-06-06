import api from "./api";

// login api
export const authService = {
  login: (data) => {
    return api.post("auth/login/", data);
  },
};