import JobSearchConfig from '../../components/JobSearchConfig';
import { useNavigate } from 'react-router-dom';

const JobSearchConfigPage = () => {
  const navigate = useNavigate();

  const handleConfigSave = (config: {
    query: string;
    location: string;
    radius: number;
    limit: number;
    start: number;
    sort: string;
    filter: number;
  }) => {
    // Aquí iría la lógica para guardar la configuración
    console.log('Configuración guardada:', config);
    // Redirigir a la página de búsqueda después de guardar
    navigate('/dashboard');
  };

  return (
    <div className="job-search-config-page">
      <JobSearchConfig onConfigSave={handleConfigSave} />
    </div>
  );
};

export default JobSearchConfigPage;
