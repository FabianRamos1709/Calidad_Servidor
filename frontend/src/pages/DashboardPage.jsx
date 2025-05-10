import { useState } from 'react';
import '../styles/DashboardPage.css';
import { Pencil, Trash2 } from 'lucide-react';

export default function DashboardPage() {
  const [items, setItems] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    item: '',
    descripcion: '',
    subcaracteristicas: [],
    puntaje: ''
  });
  const [newSubcaracteristica, setNewSubcaracteristica] = useState({
    nombre: '',
    descripcion: ''
  });
  const [expandedSubIndices, setExpandedSubIndices] = useState([]);

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubcaracteristicaChange = e => {
    setNewSubcaracteristica({ 
      ...newSubcaracteristica, 
      [e.target.name]: e.target.value 
    });
  };

  const addSubcaracteristica = () => {
    if (newSubcaracteristica.nombre && newSubcaracteristica.descripcion) {
      setFormData({
        ...formData,
        subcaracteristicas: [
          ...formData.subcaracteristicas,
          { ...newSubcaracteristica }
        ]
      });
      setNewSubcaracteristica({ nombre: '', descripcion: '' });
    }
  };

  const toggleSubcaracteristica = (index) => {
    if (expandedSubIndices.includes(index)) {
      setExpandedSubIndices(expandedSubIndices.filter(i => i !== index));
    } else {
      setExpandedSubIndices([...expandedSubIndices, index]);
    }
  };

  const handleSubmit = e => {
    e.preventDefault();
    setItems([...items, formData]);
    setFormData({
      item: '',
      descripcion: '',
      subcaracteristicas: [],
      puntaje: ''
    });
    setShowModal(false);
  };

  const openModal = () => {
    setFormData({
      item: '',
      descripcion: '',
      subcaracteristicas: [],
      puntaje: ''
    });
    setNewSubcaracteristica({ nombre: '', descripcion: '' });
    setExpandedSubIndices([]);
    setShowModal(true);
  };

  return (
    <div className="dashboard-container">
      <h1 className="title">ISO/IEC 25010</h1>
      <button className="add-button" onClick={openModal}>
        Agregar Nuevo Item
      </button>
      <table className="item-table">
        <thead>
          <tr>
            <th>ITEM</th>
            <th>DESCRIPCION</th>
            <th>SUBCARACTERÍSTICAS</th>
            <th>PORCENTAJE</th>
            <th>ACCIONES</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, idx) => (
            <tr key={idx}>
              <td>{item.item}</td>
              <td>{item.descripcion}</td>
              <td>{item.subcaracteristicas.length}</td>
              <td>{item.puntaje}%</td>
              <td>
                <button className="icon-button"><Pencil size={15}/></button>
                <button className="icon-button"><Trash2 size={15}/></button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2 className="modal-title">Nuevo Item</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Nombre del item</label>
                <input 
                  type="text" 
                  name="item" 
                  placeholder="Value" 
                  value={formData.item}
                  onChange={handleChange} 
                  required 
                />
              </div>
              
              <div className="form-group">
                <label>Descripción</label>
                <input 
                  type="text" 
                  name="descripcion" 
                  placeholder="Value" 
                  value={formData.descripcion}
                  onChange={handleChange} 
                  required 
                />
              </div>
              
              <div className="form-group">
                <label>Subcaracterísticas</label>
                
                {/* Lista de subcaracterísticas añadidas */}
                {formData.subcaracteristicas.map((sub, idx) => (
                  <div key={idx} className="subcaracteristica-item">
                    <div 
                      className="subcaracteristica-header" 
                      onClick={() => toggleSubcaracteristica(idx)}
                    >
                      <span className={`subcaracteristica-name ${!expandedSubIndices.includes(idx) ? 'highlighted' : ''}`}>
                        Subcaracterística {idx + 1}
                      </span>
                      <span className="toggle-icon">
                        {expandedSubIndices.includes(idx) ? '▼' : '►'}
                      </span>
                    </div>
                    
                    {expandedSubIndices.includes(idx) && (
                      <div className="subcaracteristica-details">
                        <div className="form-group">
                          <label>Nombre Subcaracterística</label>
                          <input 
                            type="text" 
                            value={sub.nombre} 
                            readOnly 
                          />
                        </div>
                        <div className="form-group">
                          <label>Descripcion Subcaracterística</label>
                          <input 
                            type="text" 
                            value={sub.descripcion} 
                            readOnly 
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                
                {/* Formulario para añadir nueva subcaracterística */}
                <div className="subcaracteristica-form">
                  <div className="form-group">
                    <label>Nombre Subcaracterística</label>
                    <input 
                      type="text" 
                      name="nombre" 
                      placeholder="Value" 
                      value={newSubcaracteristica.nombre}
                      onChange={handleSubcaracteristicaChange} 
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Descripcion Subcaracterística</label>
                    <input 
                      type="text" 
                      name="descripcion" 
                      placeholder="Value" 
                      value={newSubcaracteristica.descripcion}
                      onChange={handleSubcaracteristicaChange} 
                    />
                  </div>
                  
                  <button 
                    type="button" 
                    className="add-sub-button"
                    onClick={addSubcaracteristica}
                  >
                    Agregar Subcaracterística
                  </button>
                </div>
              </div>
              
              <div className="form-group">
                <label>Puntaje (%)</label>
                <input 
                  type="number" 
                  name="puntaje" 
                  placeholder="Value" 
                  value={formData.puntaje}
                  onChange={handleChange} 
                  required 
                />
              </div>
              
              <div className="modal-actions">
                <button type="button" className="cancel-button" onClick={() => setShowModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="add-item-button">
                  Agregar Item
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}