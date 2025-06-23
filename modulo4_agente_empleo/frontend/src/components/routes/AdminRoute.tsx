// src/components/AdminRoute.tsx
import React from 'react';
import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import RequireAuth from './RequireAuth';

interface Props {
  children: ReactNode;
}

const AdminRoute: React.FC<Props> = ({ children }) => {
  const role = localStorage.getItem('role');

  return (
    <RequireAuth>
      {role === 'admin' ? children : <Navigate to="/dashboard" replace />}
    </RequireAuth>
  );
};

export default AdminRoute;

