// src/pages/DashboardWrapper.tsx
import { Typography, Box } from '@mui/material';
import ChangePassword from './ChangePass';
import AdminUsers from './AdminUsers';


export default function DashboardWrapper() {
  const role = localStorage.getItem('role');

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Bienvenido al Dashboard
      </Typography>

      <Typography color="success.main" gutterBottom>
        Estás logueado correctamente 🎉
      </Typography>

      <ChangePassword />

      {role === 'admin' && <AdminUsers />}
    </Box>
  );
}
