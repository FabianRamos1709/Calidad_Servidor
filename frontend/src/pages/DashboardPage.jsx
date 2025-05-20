import { useState, useEffect } from 'react';
import '../styles/DashboardPage.css';
import { Pencil, Trash2 } from 'lucide-react';
import { useAuth } from '../context/authContext';

export default function DashboardPage() {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [expandedSubIndices, setExpandedSubIndices] = useState([]);
  const [softwares, setSoftwares] = useState([]);
  const [selectedSoftwareId, setSelectedSoftwareId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [formData, setFormData] = useState({
    software_id: '',
    name: '',
    description: '',
    weight_percentage: '',
    subcharacteristics: []
  });

  const [newSubcaracteristica, setNewSubcaracteristica] = useState({
    name: '',
    description: ''
  });

  useEffect(() => {
    if (user && user.id) {
      setIsLoading(true);
      fetch(`http://localhost:5000/software/${user.id}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(data => {
          setSoftwares(data.software || []);
          setSelectedSoftwareId(null); // No seleccionar por defecto
          setIsLoading(false);
        })
        .catch(err => {
          console.error("Error al cargar softwares:", err);
          setIsLoading(false);
        });
    }
  }, [user]);

  // Cargar ítems cuando se selecciona un software
  useEffect(() => {
    if (selectedSoftwareId) {
      setIsLoading(true);
      fetch(`http://localhost:5002/modelo/items_por_software/${selectedSoftwareId}`)
        .then(res => res.json())
        .then(data => {
          setItems(data.items || []);
          setIsLoading(false);
        })
        .catch(err => {
          console.error("Error al cargar ítems del software:", err);
          setItems([]);
          setIsLoading(false);
        });
    } else {
      setItems([]); // Limpiar si no hay software seleccionado
    }
  }, [selectedSoftwareId]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSoftwareSelect = (e) => {
    const softwareId = parseInt(e.target.value);
    setSelectedSoftwareId(softwareId);
    setFormData({ ...formData, software_id: softwareId });
  };

  const handleSubcaracteristicaChange = e => {
    setNewSubcaracteristica({ ...newSubcaracteristica, [e.target.name]: e.target.value });
  };

  const addSubcaracteristica = () => {
    if (newSubcaracteristica.name && newSubcaracteristica.description) {
      setFormData({
        ...formData,
        subcharacteristics: [...formData.subcharacteristics, { ...newSubcaracteristica }]
      });
      setNewSubcaracteristica({ name: '', description: '' });
    }
  };

  const removeSubcaracteristica = (index) => {
    const updatedSubs = [...formData.subcharacteristics];
    updatedSubs.splice(index, 1);
    setFormData({
      ...formData,
      subcharacteristics: updatedSubs
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.software_id) {
      alert("Por favor selecciona un software.");
      return;
    }
    
    setIsLoading(true);
    
    try {
      const res = await fetch("http://localhost:5002/modelo/caracteristica", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: formData.name,
          description: formData.description,
          weight_percentage: parseFloat(formData.weight_percentage),
          subcharacteristics: formData.subcharacteristics
        })
      });

      const data = await res.json();

      if (res.ok) {
        const assignRes = await fetch("http://localhost:5002/modelo/asignar_item", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            software_id: formData.software_id,
            characteristics: [data.characteristic_id]
          })
        });

        if (assignRes.ok) {
          alert("Item registrado y asignado correctamente.");

          // Volver a cargar los ítems desde el backend
          const updatedItemsRes = await fetch(`http://localhost:5002/modelo/items_por_software/${formData.software_id}`);
          const updatedItemsData = await updatedItemsRes.json();
          setItems(updatedItemsData.items || []);

          resetForm();
        }
        else {
          alert("Error al asignar ítem al software.");
        }
      } else {
        alert(data.error || "Error al registrar ítem.");
      }
    } catch (error) {
      alert("Error al conectar con el servidor");
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setShowModal(false);
    setEditMode(false);
    setEditItem(null);
    setFormData({
      software_id: selectedSoftwareId || '',
      name: '',
      description: '',
      weight_percentage: '',
      subcharacteristics: []
    });
  };

  const handleDelete = async (itemId) => {
    if (!confirm("¿Estás seguro de eliminar este ítem?")) return;
    
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:5002/modelo/caracteristica/${itemId}`, {
        method: "DELETE"
      });
      
      if (res.ok) {
        // Recargar los ítems después de eliminar
        const updatedItemsRes = await fetch(`http://localhost:5002/modelo/items_por_software/${selectedSoftwareId}`);
        const updatedItemsData = await updatedItemsRes.json();
        setItems(updatedItemsData.items || []);
        alert("Item eliminado correctamente");
      } else {
        alert("Error al eliminar el ítem");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error al conectar con el servidor");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = async (item) => {
    setEditMode(true);
    setEditItem(item);
    
    try {
      // Obtener detalles completos del ítem
      const res = await fetch(`http://localhost:5002/modelo/caracteristica/${item.id}`);
      const itemData = await res.json();
      
      setFormData({
        software_id: selectedSoftwareId,
        name: itemData.name,
        description: itemData.description,
        weight_percentage: itemData.weight_percentage,
        subcharacteristics: itemData.subcharacteristics || []
      });
      
      setShowModal(true);
    } catch (error) {
      console.error("Error al cargar detalles del ítem:", error);
      alert("Error al cargar detalles del ítem");
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!editItem) return;
    
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:5002/modelo/caracteristica/${editItem.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: formData.name,
          description: formData.description,
          weight_percentage: parseFloat(formData.weight_percentage),
          subcharacteristics: formData.subcharacteristics
        })
      });

      if (res.ok) {
        // Recargar los ítems
        const updatedItemsRes = await fetch(`http://localhost:5002/modelo/items_por_software/${selectedSoftwareId}`);
        const updatedItemsData = await updatedItemsRes.json();
        setItems(updatedItemsData.items || []);
        
        resetForm();
        alert("Item actualizado correctamente");
      } else {
        const errorData = await res.json();
        alert(errorData.message || "Error al actualizar el ítem");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error al conectar con el servidor");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h1 className="title">ISO/IEC 25010</h1>
      <div className="filter-section">
        <label>Filtrar por software:</label>
        <select value={selectedSoftwareId || ''} onChange={handleSoftwareSelect}>
          <option value="">Seleccione un software</option>
          {softwares.map(sw => (
            <option key={sw.id} value={sw.id}>{sw.name}</option>
          ))}
        </select>
      </div>
      
      {selectedSoftwareId && (
        <button 
          className="add-button" 
          onClick={() => {
            setEditMode(false);
            setFormData({
              software_id: selectedSoftwareId,
              name: '',
              description: '',
              weight_percentage: '',
              subcharacteristics: []
            });
            setShowModal(true);
          }}
        >
          Agregar Nuevo Item
        </button>
      )}

      {isLoading ? (
        <div className="loading">Cargando...</div>
      ) : (
        <table className="item-table">
          <thead>
            <tr>
              <th>SOFTWARE</th>
              <th>ITEM</th>
              <th>DESCRIPCIÓN</th>
              <th>SUBCARACTERÍSTICAS</th>
              <th>PESO (%)</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            {!selectedSoftwareId ? (
              <tr><td colSpan="6">Seleccione un software para ver sus ítems</td></tr>
            ) : items.length === 0 ? (
              <tr><td colSpan="6">No hay ítems registrados para este software.</td></tr>
            ) : (
              items.map((item) => (
                <tr key={item.id}>
                  <td>{softwares.find(s => s.id === item.software_id)?.name || "N/A"}</td>
                  <td>{item.name}</td>
                  <td>{item.description}</td>
                  <td>{item.subcharacteristics.length}</td>
                  <td>{item.weight_percentage}%</td>
                  <td>
                    <button className="icon-button" onClick={() => handleEdit(item)}><Pencil size={15} /></button>
                    <button className="icon-button" onClick={() => handleDelete(item.id)}><Trash2 size={15} /></button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2 className="modal-title">{editMode ? 'Editar Item' : 'Nuevo Item'}</h2>
            <form onSubmit={editMode ? handleUpdate : handleSubmit}>
              <div className="form-group">
                <label>Software</label>
                <select 
                  name="software_id" 
                  value={formData.software_id} 
                  onChange={handleSoftwareSelect} 
                  required
                  disabled={editMode} // No permitir cambiar el software al editar
                >
                  <option value="">Seleccione un software</option>
                  {softwares.map(sw => (
                    <option key={sw.id} value={sw.id}>{sw.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Nombre del ítem</label>
                <input type="text" name="name" value={formData.name} onChange={handleChange} required />
              </div>

              <div className="form-group">
                <label>Descripción</label>
                <textarea name="description" value={formData.description} onChange={handleChange} required />
              </div>

              <div className="form-group">
                <label>Peso (%)</label>
                <input 
                  type="number" 
                  name="weight_percentage" 
                  value={formData.weight_percentage} 
                  onChange={handleChange} 
                  min="1" 
                  max="100" 
                  required 
                />
              </div>

              <div className="form-group">
                <label>Subcaracterísticas ({formData.subcharacteristics.length})</label>
                {formData.subcharacteristics.map((sub, idx) => (
                  <div key={idx} className="subcaracteristica-item">
                    <div className="subcaracteristica-header" onClick={() => setExpandedSubIndices(expandedSubIndices.includes(idx) ? expandedSubIndices.filter(i => i !== idx) : [...expandedSubIndices, idx])}>
                      <span className="subcaracteristica-name">{sub.name}</span>
                      <span className="toggle-icon">{expandedSubIndices.includes(idx) ? '▼' : '►'}</span>
                    </div>
                    {expandedSubIndices.includes(idx) && (
                      <div className="subcaracteristica-details">
                        <div className="form-group">
                          <label>Nombre</label>
                          <input type="text" value={sub.name} readOnly />
                        </div>
                        <div className="form-group">
                          <label>Descripción</label>
                          <input type="text" value={sub.description} readOnly />
                        </div>
                        <button 
                          type="button" 
                          className="remove-sub-button"
                          onClick={() => removeSubcaracteristica(idx)}
                        >
                          Eliminar
                        </button>
                      </div>
                    )}
                  </div>
                ))}
                <div className="subcaracteristica-form">
                  <input 
                    type="text" 
                    name="name" 
                    value={newSubcaracteristica.name} 
                    onChange={handleSubcaracteristicaChange} 
                    placeholder="Nombre" 
                  />
                  <input 
                    type="text" 
                    name="description" 
                    value={newSubcaracteristica.description} 
                    onChange={handleSubcaracteristicaChange} 
                    placeholder="Descripción" 
                  />
                  <button 
                    type="button" 
                    className="add-sub-button" 
                    onClick={addSubcaracteristica}
                  >
                    Agregar Subcaracterística
                  </button>
                </div>
              </div>

              <div className="modal-actions">
                <button type="button" className="cancel-button" onClick={resetForm}>Cancelar</button>
                <button type="submit" className="add-item-button" disabled={isLoading}>
                  {isLoading ? 'Procesando...' : (editMode ? 'Guardar Cambios' : 'Agregar Item')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}