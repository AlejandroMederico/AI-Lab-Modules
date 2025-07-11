import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container, Paper, Typography, Box,
  TextField, Button, Alert, Link,
} from '@mui/material';
import { register as registerApi } from '../../api/auth';  // <-- ADAPTA ESTA RUTA

const Register = () => {
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== password2) {
      setError('Las contraseñas no coinciden');
      return;
    }

    try {
      await registerApi({ email: correo, password });  // <-- AQUÍ LLAMA BIEN
      navigate('/login');                              // Redirige
    } catch (err) {
      console.error(err);
      setError('Error al crear el usuario');
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Crear cuenta
        </Typography>

        <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
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
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Repetir contraseña"
            type="password"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            required
            fullWidth
          />

          <Button type="submit" variant="contained" color="primary">
            REGISTRARME
          </Button>

          {error && <Alert severity="error">{error}</Alert>}

          <Typography variant="body2" align="center">
            ¿Ya tenés cuenta?{' '}
            <Link component={RouterLink} to="/login">
              Iniciá sesión
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;
