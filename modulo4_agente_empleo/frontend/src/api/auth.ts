import axios from "axios";
import type { AxiosInstance } from "axios";
import qs from "qs";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

/**
 * Axios instanciado con la URL base del backend.
 * Se agrega un interceptor para adjuntar automáticamente el JWT.
 */
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

/* -------------------------------------------------------------------------- */
/*                                  Tipados                                   */
/* -------------------------------------------------------------------------- */

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  role: string;
}

/* -------------------------------------------------------------------------- */
/*                                   Auth                                     */
/* -------------------------------------------------------------------------- */

/**
 * Realiza login usando OAuth2PasswordRequestForm.
 * @param username Email del usuario (campo requerido por FastAPI)
 * @param password Contraseña del usuario
 */
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

/**
 * Ejemplo de registro por si lo necesitás (POST /register en tu backend).
 * Descomentalo y adaptalo cuando implementes ese endpoint.
 */
// export const register = async (payload: {
//   email: string;
//   password: string;
// }): Promise<void> => {
//   await api.post('/register', payload);
// };

/* -------------------------------------------------------------------------- */
/*                       Nueva función: cambiar contraseña                    */
/* -------------------------------------------------------------------------- */

export interface PasswordChangePayload {
  old_password: string;
  new_password: string;
}

export interface PasswordChangeResponse {
  msg: string; // ← según devolvimos en el backend
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

export default api;
