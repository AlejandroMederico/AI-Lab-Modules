// src/components/Navbar.tsx
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import SettingsIcon from '@mui/icons-material/Settings';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role'); // 'admin' | 'user' | null

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  const isLoginPage = location.pathname === '/login';

  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Agente IA Demo
        </Typography>

        {/* Botones condicionales */}
        {role === 'admin' && (
          <Button
            color="inherit"
            startIcon={<PeopleAltIcon />}
            onClick={() => navigate('/admin')}
          >
            Usuarios
          </Button>
        )}

        {token && (
          <>
            <Button
              color="inherit"
              startIcon={<SettingsIcon />}
              onClick={() => navigate('/settings')}
            >
              Propiedades
            </Button>

            <Button
              color="error"
              startIcon={<LogoutIcon />}
              onClick={handleLogout}
            >
              Cerrar sesión
            </Button>
          </>
        )}

        {!token && !isLoginPage && (
          <Button
            color="primary"
            variant="contained"
            startIcon={<LoginIcon />}
            onClick={() => navigate('/login')}
          >
            Iniciar sesión
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
