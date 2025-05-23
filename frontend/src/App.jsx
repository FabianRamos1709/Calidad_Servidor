import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import { AuthProvider } from './context/authContext';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegistroPage';
import DashboardPage from './pages/DashboardPage';
import RegistroSoftwarePage from './pages/RegistroSofware';
import EvaluacionSoftwarePage from './pages/EvaluacionSoftwarePage';
import ResultadosEvaluacionPage from './pages/ResultadosEvaluacionPage';
import TablaREvaluacionPage from './pages/TablaResultaod';
import RegistroRiesgoPage from './pages/RegistroRiesgoPage';
import DetalleRiesgoPage from './pages/DetalleRiesgoPage';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Auth */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/registro" element={<RegisterPage />} />

          {/* General */}
          <Route path="/home" element={<MainLayout><HomePage /></MainLayout>} />
          <Route path="/dashboard" element={<MainLayout><DashboardPage /></MainLayout>} />
          <Route path="/software" element={<MainLayout><RegistroSoftwarePage /></MainLayout>} />
          <Route path="/software/evaluar/:softwareId" element={<MainLayout><EvaluacionSoftwarePage /></MainLayout>} />

          {/* Evaluación de calidad y riesgos */}
          <Route path="/resultados" element={<MainLayout><TablaREvaluacionPage /></MainLayout>} />
          <Route path="/resultados/:softwareId/:evaluationId" element={<MainLayout><ResultadosEvaluacionPage /></MainLayout>} />

          {/* Evaluación de riesgos */}
          <Route path="/riesgos/registrar/:softwareId" element={<MainLayout><RegistroRiesgoPage /></MainLayout>} />
          <Route path="/riesgos/detalle/:softwareId/:riskId" element={<MainLayout><DetalleRiesgoPage /></MainLayout>} />

          {/* Redirección y 404 */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="*" element={
            <MainLayout>
              <div style={{ height: '50vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <h1>404</h1>
                <p>Página no encontrada</p>
              </div>
            </MainLayout>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
