// src/components/RequireAuth.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { isTokenValid } from '../../utils/auth';

interface Props {
  children: React.ReactNode;
}

const RequireAuth: React.FC<Props> = ({ children }) => {
  const token = localStorage.getItem('token');
  const location = useLocation();

  if (!isTokenValid(token)) {
    localStorage.removeItem('token');
    localStorage.removeItem('role');

    return <Navigate to="/login" state={{ expired: true, from: location }} replace />;
  }

  return <>{children}</>;
};

export default RequireAuth;
