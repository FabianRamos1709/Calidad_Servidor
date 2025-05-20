// EvaluationPage.jsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Pencil, CheckCircle, ChevronDown, ChevronRight } from 'lucide-react';
import '../styles/EvaluationPage.css';

export default function EvaluationPage() {
  const { softwareId } = useParams();
  const [evaluationData, setEvaluationData] = useState(null);
  const [scores, setScores] = useState({});
  const [expandedCharacteristics, setExpandedCharacteristics] = useState([]);
  const [comments, setComments] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Estructura basada en la plantilla Excel ISO/IEC 25010
  const characteristics = [
    {
      id: 1,
      name: 'Funcionalidad',
      description: 'Capacidad del software de proveer funciones que satisfacen necesidades explícitas e implícitas.',
      percentage: 14,
      subcharacteristics: [
        { id: 1.1, name: 'Adecuación', description: 'El software provee un conjunto adecuado de funciones para las tareas especificadas.' },
        { id: 1.2, name: 'Exactitud', description: 'El software provee resultados con el grado necesario de precisión.' },
        { id: 1.3, name: 'Interoperabilidad', description: 'Capacidad de interactuar con otros sistemas especificados.' },
        { id: 1.4, name: 'Seguridad', description: 'Protege información y datos de accesos no autorizados.' },
        { id: 1.5, name: 'Conformidad', description: 'Adherencia a estándares y regulaciones.' }
      ]
    },
    {
      id: 2,
      name: 'Fiabilidad',
      description: 'Capacidad del software de mantener un nivel específico de funcionamiento.',
      percentage: 14,
      subcharacteristics: [
        { id: 2.1, name: 'Madurez', description: 'Evita fallas como resultado de errores en el software.' },
        { id: 2.2, name: 'Tolerancia a errores', description: 'Mantiene funcionamiento ante errores.' },
        { id: 2.3, name: 'Recuperabilidad', description: 'Restablece funcionamiento después de fallas.' },
        { id: 2.4, name: 'Conformidad', description: 'Adherencia a normas de fiabilidad.' }
      ]
    },
    // ... Agregar las demás características (Usabilidad, Eficiencia, etc.)
  ];

  useEffect(() => {
    // Simular carga de datos
    const loadData = async () => {
      // Aquí iría la llamada a la API para cargar los datos del software
      setEvaluationData({
        id: softwareId,
        name: 'Software Ejemplo',
        date: new Date().toISOString().split('T')[0]
      });
      
      // Inicializar scores y comentarios
      const initialScores = {};
      const initialComments = {};
      
      characteristics.forEach(char => {
        char.subcharacteristics.forEach(sub => {
          initialScores[sub.id] = 0;
          initialComments[sub.id] = '';
        });
      });
      
      setScores(initialScores);
      setComments(initialComments);
    };
    
    loadData();
  }, [softwareId]);

  const toggleCharacteristic = (charId) => {
    if (expandedCharacteristics.includes(charId)) {
      setExpandedCharacteristics(expandedCharacteristics.filter(id => id !== charId));
    } else {
      setExpandedCharacteristics([...expandedCharacteristics, charId]);
    }
  };

  const handleScoreChange = (subId, value) => {
    setScores(prev => ({
      ...prev,
      [subId]: parseInt(value)
    }));
  };

  const handleCommentChange = (subId, value) => {
    setComments(prev => ({
      ...prev,
      [subId]: value
    }));
  };

  const calculateCharacteristicScore = (charId) => {
    const char = characteristics.find(c => c.id === charId);
    if (!char) return 0;
    
    const subScores = char.subcharacteristics.map(sub => scores[sub.id] || 0);
    const total = subScores.reduce((sum, score) => sum + score, 0);
    const maxPossible = char.subcharacteristics.length * 3; // 3 es el máximo puntaje por subcaracterística
    
    return maxPossible > 0 ? Math.round((total / maxPossible) * 100) : 0;
  };

  const calculateGlobalScore = () => {
    let totalWeighted = 0;
    
    characteristics.forEach(char => {
      const charScore = calculateCharacteristicScore(char.id);
      totalWeighted += (charScore * char.percentage) / 100;
    });
    
    return Math.round(totalWeighted);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    try {
      // Preparar datos para enviar al backend
      const evaluationDetails = [];
      
      characteristics.forEach(char => {
        char.subcharacteristics.forEach(sub => {
          evaluationDetails.push({
            characteristic_id: char.id,
            subcharacteristic_id: sub.id,
            score: scores[sub.id],
            comment: comments[sub.id],
            characteristic_percentage: char.percentage
          });
        });
      });
      
      const payload = {
        software_id: softwareId,
        details: evaluationDetails
      };
      
      // Aquí iría la llamada a la API para guardar la evaluación
      console.log('Enviando evaluación:', payload);
      // await api.post('/evaluacion/evaluar', payload);
      
      alert('Evaluación guardada exitosamente!');
    } catch (error) {
      console.error('Error al guardar evaluación:', error);
      alert('Error al guardar la evaluación');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!evaluationData) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="evaluation-container">
      <div className="evaluation-header">
        <h1>Evaluación de Software: {evaluationData.name}</h1>
        <div className="evaluation-meta">
          <span>Fecha: {evaluationData.date}</span>
          <span>ID: {evaluationData.id}</span>
        </div>
      </div>
      
      <div className="characteristics-list">
        {characteristics.map(char => (
          <div key={char.id} className="characteristic-card">
            <div 
              className="characteristic-header"
              onClick={() => toggleCharacteristic(char.id)}
            >
              <div className="characteristic-title">
                <span className="toggle-icon">
                  {expandedCharacteristics.includes(char.id) ? <ChevronDown /> : <ChevronRight />}
                </span>
                <h2>{char.name}</h2>
                <span className="percentage-badge">{char.percentage}%</span>
              </div>
              <div className="characteristic-score">
                <span>Puntaje: {calculateCharacteristicScore(char.id)}%</span>
              </div>
            </div>
            
            {expandedCharacteristics.includes(char.id) && (
              <div className="subcharacteristics-list">
                <p className="characteristic-description">{char.description}</p>
                
                <table className="evaluation-table">
                  <thead>
                    <tr>
                      <th>Subcaracterística</th>
                      <th>Descripción</th>
                      <th>Puntaje (0-3)</th>
                      <th>Observaciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {char.subcharacteristics.map(sub => (
                      <tr key={sub.id}>
                        <td>{sub.name}</td>
                        <td>{sub.description}</td>
                        <td>
                          <select
                            value={scores[sub.id] || 0}
                            onChange={(e) => handleScoreChange(sub.id, e.target.value)}
                            className="score-select"
                          >
                            <option value="0">0 - No cumple</option>
                            <option value="1">1 - Cumple parcialmente</option>
                            <option value="2">2 - Cumple adecuadamente</option>
                            <option value="3">3 - Cumple totalmente</option>
                          </select>
                        </td>
                        <td>
                          <input
                            type="text"
                            value={comments[sub.id] || ''}
                            onChange={(e) => handleCommentChange(sub.id, e.target.value)}
                            placeholder="Ingrese observaciones..."
                            className="comment-input"
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="evaluation-summary">
        <div className="global-score">
          <h3>Puntaje Global</h3>
          <div className="score-circle">
            <span>{calculateGlobalScore()}%</span>
          </div>
          <div className="score-description">
            {calculateGlobalScore() >= 90 && <span className="excellent">Excelente</span>}
            {calculateGlobalScore() >= 71 && calculateGlobalScore() < 90 && <span className="outstanding">Sobresaliente</span>}
            {calculateGlobalScore() >= 51 && calculateGlobalScore() < 71 && <span className="acceptable">Aceptable</span>}
            {calculateGlobalScore() >= 31 && calculateGlobalScore() < 51 && <span className="insufficient">Insuficiente</span>}
            {calculateGlobalScore() <= 30 && <span className="deficient">Deficiente</span>}
          </div>
        </div>
        
        <div className="evaluation-actions">
          <button className="save-draft">Guardar Borrador</button>
          <button 
            className="submit-evaluation"
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Enviando...' : (
              <>
                <CheckCircle size={18} /> Finalizar Evaluación
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}