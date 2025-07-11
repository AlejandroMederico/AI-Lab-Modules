import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Alert,
  Box,
} from '@mui/material';
import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';          // 👈  nuevo
import { changePassword } from '../../api/auth';
import type { AxiosError } from 'axios';

const ChangePassword = () => {
  const [oldPass, setOldPass] = useState('');
  const [newPass, setNewPass] = useState('');
  const [msg, setMsg] = useState('');
  const [severity, setSeverity] =
    useState<'success' | 'error' | 'warning'>('success');

  const navigate = useNavigate();                        // 👈  nuevo

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMsg('');

    try {
      const { msg } = await changePassword({
        old_password: oldPass,
        new_password: newPass,
      });

      // 🟢 Éxito
      setMsg(`✅ ${msg}. Serás redirigido al login…`);
      setSeverity('success');

      // 1️⃣ Limpiamos campos
      setOldPass('');
      setNewPass('');

      // 2️⃣ Eliminamos token
      localStorage.removeItem('token');
      localStorage.removeItem('role');

      // 3️⃣ Esperamos 1 s y navegamos
      setTimeout(() => navigate('/login'), 1000);

    } catch (err) {
      const error = err as AxiosError<{ detail?: string }>;
      const errMsg =
        error.response?.data?.detail || error.message || 'Error desconocido';
      setMsg(`❌ ${errMsg}`);
      setSeverity('error');
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Cambiar Contraseña
        </Typography>

        <Box
          component="form"
          onSubmit={handleSubmit}
          display="flex"
          flexDirection="column"
          gap={2}
        >
          <TextField
            label="Contraseña actual"
            type="password"
            value={oldPass}
            onChange={(e) => setOldPass(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Nueva contraseña"
            type="password"
            value={newPass}
            onChange={(e) => setNewPass(e.target.value)}
            required
            fullWidth
          />
          <Button type="submit" variant="contained" color="primary">
            Guardar
          </Button>

          {msg && (
            <Alert severity={severity} onClose={() => setMsg('')}>
              {msg}
            </Alert>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default ChangePassword;
