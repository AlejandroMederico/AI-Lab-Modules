// src/App.tsx
import { Container } from '@mui/material';
import { Routes, Route, Navigate } from 'react-router-dom';

import Navbar from './components/layout/Navbar';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import UserDashboardWrapper from './pages/dashboard/UserDashboardWrapper';
import AdminPanelWrapper from './pages/dashboard/AdminPanelWrapper';
import RequireAuth from './components/routes/RequireAuth';
import AdminRoute from './components/routes/AdminRoute';
import ChangePass from './pages/dashboard/ChangePass';


export default function App() {
  return (
    <Container disableGutters maxWidth={false}>
      <Navbar />  {/* ← siempre visible */}

      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* dashboard para usuarios autenticados */}
        <Route path="/dashboard/*" element={
          <RequireAuth>
            <UserDashboardWrapper />
          </RequireAuth>
        } />

        {/* panel exclusivo para admins */}
        <Route path="/admin" element={
          <AdminRoute>
            <AdminPanelWrapper />
          </AdminRoute>
        } />

        {/* settings */}
        <Route path="/settings" element={
          <RequireAuth>
            <ChangePass />
          </RequireAuth>
        } />
      </Routes>
    </Container>
  );
}
