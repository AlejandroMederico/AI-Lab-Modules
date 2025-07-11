import api from "./auth"; // ← reutilizamos la instancia con token
/* -------------------------------------------------------------------------- */
/*                             Tipado de usuario                              */
/* -------------------------------------------------------------------------- */
export interface UserRecord {
  id: number;
  email: string;
  role: "admin" | "user";
}

/* -------------------------------------------------------------------------- */
/*                                Endpoints                                   */
/* -------------------------------------------------------------------------- */
export const listUsers = async (): Promise<UserRecord[]> => {
  const { data } = await api.get<UserRecord[]>("/users");
  return data;
};

export const updateUser = async (
  id: number,
  payload: Partial<Omit<UserRecord, "id">>
): Promise<UserRecord> => {
  const { data } = await api.patch<UserRecord>(`/users/${id}`, payload);
  return data;
};

export const deleteUser = async (id: number): Promise<void> => {
  await api.delete(`/users/${id}`);
};
