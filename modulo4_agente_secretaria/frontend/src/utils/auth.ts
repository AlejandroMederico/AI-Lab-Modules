// src/utils/auth.ts
import { jwtDecode } from "jwt-decode";

interface JwtPayload {
  exp: number; // Unix timestamp (segundos)
  // …otros campos si querés tiparlos
}

export const isTokenValid = (token: string | null): boolean => {
  if (!token) return false;

  try {
    const { exp } = jwtDecode<JwtPayload>(token);
    // multiplica por 1000 porque Date.now() está en milisegundos
    return exp * 1000 > Date.now();
  } catch {
    // token malformado
    return false;
  }
};
