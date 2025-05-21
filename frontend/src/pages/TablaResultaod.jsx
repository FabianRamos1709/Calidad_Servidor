import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/ResultadosTabla.css';

export default function ResultadosTabla() {
  const navigate = useNavigate();
  const [datos, setDatos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Obtén el user_id de donde sea apropiado en tu aplicación
  // Por ejemplo, podrías obtenerlo del localStorage o de un contexto
  const userId = localStorage.getItem('userId') || '1'; // Valor por defecto '1' para pruebas
  
  useEffect(() => {
    const fetchSoftwareEvaluados = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5003/evaluacion/software-evaluados/${userId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // Agrega aquí cualquier header adicional que necesites, como token de autenticación
            // 'Authorization': `Bearer ${token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Error en la petición: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Asumiendo que la respuesta tiene el formato esperado
        // según el servidor Flask que proporcionaste
        const softwareFormateado = data.map(item => ({
          codigo: item.software_id,
          nombreSoftware: item.software_name,
          fechaEvaluacion: item.evaluation_date,
          porcentajeGlobal: item.global_percentage,
          resultado: item.result,
          evaluationId: item.evaluation_id
        }));
        
        setDatos(softwareFormateado);
        setError(null);
      } catch (err) {
        console.error("Error al obtener los datos:", err);
        setError("No se pudieron cargar los resultados. Intente más tarde.");
        // No establecemos datos de ejemplo en caso de error
        setDatos([]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchSoftwareEvaluados();
  }, [userId]); // La dependencia es userId para que se vuelva a ejecutar si cambia

  // Redirigir a la página de detalle
  const handleVerDetalle = (softwareId, evaluationId) => {
    navigate(`/resultados/${softwareId}/${evaluationId}`);
  };

  const handleDescargarReporte = (codigo) => {
    console.log(`Descargar reporte del software con código: ${codigo}`);
    // Aquí puedes implementar la lógica para descargar el reporte
  };

  return (
    <div className="container">
      <h1 className="titulo">Resultados</h1>
      {loading ? (
        <p>Cargando resultados...</p>
      ) : error ? (
        <p className="error-mensaje">{error}</p>
      ) : (
        <div className="tabla-container">
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>CODIGO</th>
                <th>Nombre del Software</th>
                <th>Fecha de Evaluación</th>
                <th>Porcentaje Global</th>
                <th>Resultado</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              {datos.map((item) => (
                <tr key={item.codigo}>
                  <td>{item.codigo}</td>
                  <td>{item.nombreSoftware}</td>
                  <td>{item.fechaEvaluacion}</td>
                  <td>{item.porcentajeGlobal}</td>
                  <td>{item.resultado}</td>
                  <td className="acciones">
                    <button
                      onClick={() => handleVerDetalle(item.codigo, item.evaluationId)}
                      className="boton-accion boton-detalle"
                      title="Ver detalle"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                      </svg>
                    </button>
                    <button
                      onClick={() => handleDescargarReporte(item.codigo)}
                      className="boton-accion boton-descargar"
                      title="Descargar reporte"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                  </td>
                </tr>
              ))}
              {datos.length === 0 && (
                <tr>
                  <td colSpan="6" className="no-datos">No hay resultados disponibles</td>
                </tr>
              )}
              {datos.length > 0 && Array(Math.max(0, 8 - datos.length)).fill().map((_, index) => (
                <tr key={`empty-${index}`} className="fila-vacia">
                  <td colSpan="6"></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="paginacion">
        <button className="boton-pagina anterior">&lt;</button>
        <button className="boton-pagina siguiente">&gt;</button>
      </div>
    </div>
  );
}