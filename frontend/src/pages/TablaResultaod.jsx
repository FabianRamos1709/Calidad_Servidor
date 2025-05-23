import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/ResultadosTabla.css';

export default function ResultadosTabla() {
  const navigate = useNavigate();
  const [datos, setDatos] = useState([]);
  const [tipoResultado, setTipoResultado] = useState('calidad'); // calidad o riesgos
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Obtener userId del localStorage o del token
  const getUserId = () => {
    const userId = localStorage.getItem('userId');
    if (userId) return userId;
    
    // Si no hay userId, intentar obtenerlo del token
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        return tokenPayload.user_id || tokenPayload.id || tokenPayload.sub || '1';
      } catch (e) {
        console.error('Error al decodificar token:', e);
        return '1';
      }
    }
    return '1';
  };

  const userId = getUserId();

  useEffect(() => {
    const fetchResultados = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let url = tipoResultado === 'calidad'
          ? `http://localhost:5003/evaluacion/software-evaluados/${userId}`
          : `http://localhost:5004/riesgo/evaluaciones/${userId}`;

        console.log(`Fetching from: ${url}`); // Para debugging

        const response = await fetch(url, {
          method: 'GET',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Agregar token si es necesario
          }
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Datos recibidos:', data); // Para debugging

        const formateado = tipoResultado === 'calidad'
          ? data.map(item => ({
              tipo: 'calidad',
              codigo: item.software_id,
              nombreSoftware: item.software_name,
              fechaEvaluacion: item.evaluation_date,
              porcentajeGlobal: item.global_percentage,
              resultado: item.result,
              evaluationId: item.evaluation_id
            }))
          : data.map(item => ({
              tipo: 'riesgo',
              codigo: item.software_id,
              nombreSoftware: item.software_name,
              fechaEvaluacion: item.evaluation_date,
              porcentajeGlobal: item.valor_riesgo || 'N/A',
              resultado: item.zona_riesgo,
              riskId: item.risk_id
            }));

        setDatos(formateado);
        setError(null);
      } catch (err) {
        console.error("Error al obtener los datos:", err);
        setError(`No se pudieron cargar los resultados: ${err.message}`);
        setDatos([]);
      } finally {
        setLoading(false);
      }
    };

    fetchResultados();
  }, [userId, tipoResultado]);

  const handleVerDetalle = (item) => {
    if (item.tipo === 'calidad') {
      navigate(`/resultados/${item.codigo}/${item.evaluationId}`);
    } else {
      navigate(`/riesgos/detalle/${item.codigo}/${item.riskId}`);
    }
  };
  const handleDescargarReporte = (codigo) => {
    console.log(`Descargar reporte del software con código: ${codigo}`);
    // Aquí puedes implementar la lógica para descargar el reporte
  };
  return (
    <div className="container">
      <h1 className="titulo">Resultados</h1>

      <div className="selector-tipo">
        <label htmlFor="tipo-select">Tipo de Resultado:</label>
        <select id="tipo-select" value={tipoResultado} onChange={e => setTipoResultado(e.target.value)}>
          <option value="calidad">Evaluación de Calidad</option>
          <option value="riesgo">Evaluación de Riesgos</option>
        </select>
      </div>

      {loading ? (
        <p>Cargando resultados...</p>
      ) : error ? (
        <div className="error-mensaje">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Reintentar</button>
        </div>
      ) : (
        <div className="tabla-container">
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>CODIGO</th>
                <th>Nombre del Software</th>
                <th>Fecha de Evaluación</th>
                <th>{tipoResultado === 'riesgo' ? 'Valor de Riesgo' : 'Porcentaje Global'}</th>
                <th>Resultado</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              {datos.map((item, index) => (
                <tr key={`${item.codigo}-${item.resultado}-${index}`}>
                  <td>{item.codigo}</td>
                  <td>{item.nombreSoftware}</td>
                  <td>{item.fechaEvaluacion}</td>
                  <td>{item.porcentajeGlobal}</td>
                  <td>{item.resultado}</td>
                  <td className="acciones">
                    <button
                      onClick={() => handleVerDetalle(item)}
                      className="boton-accion boton-detalle"
                      title="Ver detalle"
                    >
                      🔍
                    </button>
                    <button
                      onClick={() => handleDescargarReporte(item.codigo)}
                      className="boton-accion boton-descargar"
                      title="Descargar reporte"
                    >⬇️</button>
                  </td>
                </tr>
              ))}
              {datos.length === 0 && (
                <tr>
                  <td colSpan="6" className="no-datos">
                    {tipoResultado === 'riesgo' 
                      ? 'No hay evaluaciones de riesgo disponibles' 
                      : 'No hay evaluaciones de calidad disponibles'
                    }
                  </td>
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
    </div>
  );
}