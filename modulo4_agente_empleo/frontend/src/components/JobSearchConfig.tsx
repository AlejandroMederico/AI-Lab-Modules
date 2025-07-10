import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Select,
  MenuItem,
  Button,
  FormControl,
  InputLabel,
} from '@mui/material';

interface JobSearchConfigProps {
  onConfigSave: (config: JobSearchRequest) => void;
}

interface JobSearchRequest {
  query: string;
  location: string;
  radius: number;
  limit: number;
  start: number;
  sort: string;
  filter: number;
}

const JobSearchConfig: React.FC<JobSearchConfigProps> = ({ onConfigSave }) => {
  const [searchConfig, setSearchConfig] = useState<JobSearchRequest>({
    query: "desarrollador python",
    location: "Buenos Aires",
    radius: 25,
    limit: 50,
    start: 0,
    sort: "date",
    filter: 0
  });

  const radiusOptions = [
    { value: 0, label: "Cualquier distancia" },
    { value: 5, label: "5 km" },
    { value: 10, label: "10 km" },
    { value: 25, label: "25 km" },
    { value: 50, label: "50 km" },
    { value: 100, label: "100 km" }
  ];

  const sortOptions = [
    { value: "date", label: "Más recientes" },
    { value: "relevance", label: "Relevancia" }
  ];

  const filterOptions = [
    { value: 0, label: "Cualquier fecha" },
    { value: 1, label: "Últimas 24 horas" },
    { value: 2, label: "Últimos 3 días" },
    { value: 3, label: "Últimos 7 días" }
  ];

  const handleChange = (name: string, value: string | number) => {
    setSearchConfig(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const saveConfig = () => {
    onConfigSave(searchConfig);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
      <Typography variant="h4" component="h2" gutterBottom>
        Configuración de Búsqueda de Empleo
      </Typography>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          label="Puesto de trabajo"
          name="query"
          value={searchConfig.query}
          onChange={(e) => handleChange('query', e.target.value)}
          placeholder="Ej: desarrollador python"
          variant="outlined"
          size="small"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          label="Ubicación"
          name="location"
          value={searchConfig.location}
          onChange={(e) => handleChange('location', e.target.value)}
          placeholder="Ej: Buenos Aires"
          variant="outlined"
          size="small"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl fullWidth size="small" variant="outlined">
          <InputLabel>Radio de búsqueda</InputLabel>
          <Select
            name="radius"
            value={searchConfig.radius}
            onChange={(e) => handleChange('radius', e.target.value)}
            label="Radio de búsqueda"
          >
            {radiusOptions.map(option => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl fullWidth size="small" variant="outlined">
          <InputLabel>Ordenar por</InputLabel>
          <Select
            name="sort"
            value={searchConfig.sort}
            onChange={(e) => handleChange('sort', e.target.value)}
            label="Ordenar por"
          >
            {sortOptions.map(option => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl fullWidth size="small" variant="outlined">
          <InputLabel>Filtrar por fecha</InputLabel>
          <Select
            name="filter"
            value={searchConfig.filter}
            onChange={(e) => handleChange('filter', e.target.value)}
            label="Filtrar por fecha"
          >
            {filterOptions.map(option => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Button
        variant="contained"
        onClick={saveConfig}
        fullWidth
      >
        Guardar Configuración
      </Button>
    </Box>
  );
};

export default JobSearchConfig;
