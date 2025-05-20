import { useState, useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
import '../styles/LoginPage.css';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const { darkMode } = useContext(ThemeContext);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5001/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        localStorage.setItem('token', result.token);
        login(result.user); // Guardar datos del usuario
        navigate("/home");
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      alert("Error de conexión con el servidor");
    }

  };

  return (
    <div className={`login-container ${darkMode ? 'dark-mode' : ''}`}>
      <div className="login-left">
        <div className="brand-content">
          <div className="logo-circle"></div>
          <h1>Design with us</h1>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
            lobortis maximus nunc, ac rhoncus odio congue quis. Sed ac semper orci, eu
            porttitor lacus.
          </p>
        </div>
      </div>
      
      <div className="login-right">
        <div className="login-form-container">
          <h2>Iniciar Sesión</h2>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Correo electrónico</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Contraseña</label>
              <div className="password-input-container">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <button 
                  type="button" 
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "Ocultar" : "Mostrar"}
                </button>
              </div>
              <a href="#" className="forgot-password">¿Olvidaste tu Contraseña?</a>
            </div>
            
            <button type="submit" className="login-button">
              Iniciar Sesión
            </button>
          </form>
          
          <div className="register-prompt">
            <span>No tienes cuenta?</span>
            <Link to="/registro">Regístrate</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;