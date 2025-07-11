import axios from "axios";
import type { AxiosInstance } from "axios";
import qs from "qs";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token && config.headers) {
    (config.headers as Record<string, string>)[
      "Authorization"
    ] = `Bearer ${token}`;
  }
  return config;
});

/* ---------------------- Tipado de respuesta de login ---------------------- */
export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  role: string;
}

/* --------------------------------- Auth ---------------------------------- */
export const login = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  const data = qs.stringify({ username, password });
  const { data: resp } = await api.post<LoginResponse>("/login", data, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return resp;
};

export const register = async (payload: {
  email: string;
  password: string;
}): Promise<void> => {
  await api.post("/register", payload);
};

export interface PasswordChangePayload {
  old_password: string;
  new_password: string;
}

export interface PasswordChangeResponse {
  msg: string;
}

export const changePassword = async (
  payload: PasswordChangePayload
): Promise<PasswordChangeResponse> => {
  const { data } = await api.post<PasswordChangeResponse>(
    "/users/me/password",
    payload
  );
  return data;
};

/* -------------------------- Login con Google JWT -------------------------- */
export const loginWithGoogle = async (
  firebaseToken: string
): Promise<LoginResponse> => {
  const { data } = await api.post<LoginResponse>("/auth/google", {
    id_token: firebaseToken,
  });
  return data;
};

export default api;
