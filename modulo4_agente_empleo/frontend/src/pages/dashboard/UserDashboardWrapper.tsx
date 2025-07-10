import Dashboard from './Dashboard';
import JobSearchConfigPage from './JobSearchConfigPage';
import { Routes, Route, Navigate } from 'react-router-dom';


const UserDashboardWrapper = () => {
  return (
    <Routes>
      <Route path="" element={<Dashboard />} />
      <Route path="configuracion-busqueda" element={<JobSearchConfigPage />} />
      <Route path="*" element={<Navigate to="" replace />} />
    </Routes>
  );
};

export default UserDashboardWrapper;
