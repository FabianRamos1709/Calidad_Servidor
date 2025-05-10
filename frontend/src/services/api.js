// Archivo para manejar todas las llamadas a la API de Flask

// URL base de tu API Flask
const API_URL = 'http://localhost:5000/api';

// Función auxiliar para hacer solicitudes
const fetchWithAuth = async (endpoint, options = {}) => {
  // Obtener el token del almacenamiento local (si existe)
  const token = localStorage.getItem('token');
  
  // Configuración por defecto
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  };
  
  // Combinar las opciones
  const fetchOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...(options.headers || {}),
    },
  };
  
  try {
    const response = await fetch(`${API_URL}${endpoint}`, fetchOptions);
    
    // Si la respuesta no es exitosa
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Ocurrió un error en la solicitud');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error en la solicitud API:', error);
    throw error;
  }
};

// Servicios de autenticación
export const authService = {
  login: async (credentials) => {
    return fetchWithAuth('/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },
  
  register: async (userData) => {
    return fetchWithAuth('/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: () => {
    return JSON.parse(localStorage.getItem('user'));
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

// Aquí puedes agregar más servicios para diferentes recursos
// Por ejemplo:

/*
export const userService = {
  getProfile: async () => {
    return fetchWithAuth('/user/profile');
  },
  
  updateProfile: async (userData) => {
    return fetchWithAuth('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  },
};
*/

export default {
  auth: authService,
  // Agregar más servicios aquí
};