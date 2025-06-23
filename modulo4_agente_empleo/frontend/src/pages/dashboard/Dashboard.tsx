import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>
        Bienvenido al Dashboard
      </Typography>
      <Typography variant="body1" gutterBottom>
        Estás logueado correctamente 🎉
      </Typography>

      <Button variant="contained" color="secondary" onClick={handleLogout}>
        Cerrar sesión
      </Button>
    </Container>
  );
};

export default Dashboard;
