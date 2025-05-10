import { useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
import Navbar from './Navbar';
import Footer from './Footer';
import DarkModeToggle from './DarkModeToggle';

export default function MainLayout({ children }) {
  const location = useLocation();
  const { darkMode } = useContext(ThemeContext);
  
  // No mostrar navbar ni footer en login y registro
  const isAuthPage = location.pathname === '/login' || location.pathname === '/registro';
  
  return (
    <div className={`page-container ${darkMode ? 'dark-theme' : ''}`}>
      {!isAuthPage && (
        <>
          {/* Fondo con overlay para páginas que no son de autenticación */}
          <div className="background"></div>
          
          {/* Contenido principal */}
          <div className="content">
            <Navbar />
            <main className="main-content">
              {children}
            </main>
            <Footer />
          </div>
        </>
      )}
      
      {isAuthPage && (
        // Para páginas de autenticación, solo renderizamos el contenido y el botón de tema
        <>
          <div className="theme-toggle-auth-pages">
            <DarkModeToggle />
          </div>
          {children}
        </>
      )}
    </div>
  );
}