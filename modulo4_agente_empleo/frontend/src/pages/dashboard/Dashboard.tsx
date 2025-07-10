import {
  Typography,
  Container,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  const handleConfiguracion = () => {
    navigate('/dashboard/configuracion-busqueda');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 8, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Bienvenido al Dashboard
      </Typography>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <Typography variant="h5" gutterBottom>
            Configuración de Búsqueda de Empleo
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Configura tus preferencias de búsqueda para encontrar los mejores empleos.
          </Typography>
          <Button variant="contained" onClick={handleConfiguracion}>
            Ir a Configuración
          </Button>
        </div>

        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <Typography variant="h5" gutterBottom>
            Últimas Búsquedas
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Aquí aparecerán tus últimas búsquedas de empleo.
          </Typography>
        </div>

        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <Typography variant="h5" gutterBottom>
            Estadísticas
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Aquí aparecerán estadísticas sobre tus búsquedas y aplicaciones.
          </Typography>
        </div>

        <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
          <Button variant="contained" color="secondary" onClick={handleLogout}>
            Cerrar sesión
          </Button>
        </div>
      </div>
    </Container>
  );
};

export default Dashboard;
