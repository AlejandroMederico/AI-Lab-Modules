import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';   // 👈
import { login as loginApi } from '../api/auth';
import { Link as RouterLink } from 'react-router-dom';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Paper,
  Alert,
  Link,
} from '@mui/material';

const Login = () => {
  const [correo, setCorreo] = useState('');
  const [contrasena, setContrasena] = useState('');

  // Usamos un solo estado para el mensaje y el tipo de alerta
  const [alertMsg, setAlertMsg] = useState('');
  const [severity, setSeverity] = useState<'error' | 'warning'>('error');

  const navigate = useNavigate();
  const location = useLocation();                       // 👈

  // 🔔 Si venimos redirigidos por expiración de sesión
  useEffect(() => {
    if (location.state?.expired) {
      setAlertMsg('⚠️ Se cerró la sesión. Iniciá sesión de nuevo.');
      setSeverity('warning');
    }
  }, [location.state]);

  useEffect(() => {
  if (alertMsg) {
      const timeout = setTimeout(() => setAlertMsg(''), 5000);
      return () => clearTimeout(timeout);
    }
  }, [alertMsg]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setAlertMsg('');

    try {
      const { access_token, role } = await loginApi(correo, contrasena);
      localStorage.setItem('role', role);
      localStorage.setItem('token', access_token);
      // 👉 redirigimos según el rol
      navigate(role === 'admin' ? '/admin' : '/dashboard');
    } catch (err) {
      console.error(err);
      setAlertMsg('Correo o contraseña incorrectos');
      setSeverity('error');
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Iniciar sesión
        </Typography>

        <Box
          component="form"
          onSubmit={handleSubmit}
          display="flex"
          flexDirection="column"
          gap={2}
        >
          <TextField
            label="Correo"
            type="email"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Contraseña"
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            required
            fullWidth
          />
          <Button type="submit" variant="contained" color="primary">
            ENTRAR
          </Button>

          <Typography variant="body2" align="center">
            ¿No tenés cuenta?{' '}
            <Link component={RouterLink} to="/register">
              Registrate aquí
            </Link>
          </Typography>

          {/* Alerta reutilizable */}
          {alertMsg && (
            <Alert
              severity={severity}
              onClose={() => setAlertMsg('')}
              sx={{ mt: 1 }}
            >
              {alertMsg}
            </Alert>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;
