import { useState, useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
import '../styles/RegistroPage.css';
import { Link } from 'react-router-dom';
import '../styles/global.css';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [passwordError, setPasswordError] = useState('');
  const { darkMode } = useContext(ThemeContext);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (name === 'password') {
      const { value } = e.target;
      setPasswordChecklist({
        length: value.length >= 8,
        uppercase: /[A-Z]/.test(value),
        number: /\d/.test(value),
        special: /[@$!%*?&#]/.test(value)
      });
    }
  };

  const validatePassword = (password) => {
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;
    return regex.test(password);
  };
  
  const [passwordChecklist, setPasswordChecklist] = useState({
    length: false,
    uppercase: false,
    number: false,
    special: false
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setPasswordError('Las contraseñas no coinciden');
      return;
    }

    if (!validatePassword(formData.password)) {
      setPasswordError('La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo');
      return;
    }

    setPasswordError('');
    console.log('Datos enviados:', formData);
    // fetch(...) aquí va tu lógica de registro
  };

  return (
    <div className={`login-container register-layout ${darkMode ? 'dark-mode' : ''}`}>
      <div className="login-right">
        <div className="login-form-container">
          <h2>Crear Cuenta</h2>

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
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Contraseña</label>
              <input
                type={showPassword ? "text" : "password"}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
            
            {passwordError && <p style={{ color: 'red', fontSize: '0.9rem' }}>{passwordError}</p>}

            <button type="submit" className="login-button">Registrarse</button>
          </form>
          
          <ul className="password-checklist">
            <li className={passwordChecklist.length ? 'valid' : 'invalid'}>
              8+ caracteres
            </li>
            <li className={passwordChecklist.uppercase ? 'valid' : 'invalid'}>
              1 mayúscula
            </li>
            <li className={passwordChecklist.number ? 'valid' : 'invalid'}>
              1 número
            </li>
            <li className={passwordChecklist.special ? 'valid' : 'invalid'}>
              1 símbolo
            </li>
          </ul>

          <div className="register-prompt">
            <span>¿Ya tienes cuenta?</span>
            <Link to="/Login">Inicia Sesión</Link>
          </div>
        </div>
      </div>

      <div className="login-left">
        <div className="brand-content">
          <div className="logo-circle"></div>
          <h1>Únete a nosotros</h1>
          <p>
            Comienza tu viaje con nosotros. Explora, crea y colabora con diseñadores e ingenieros como tú.
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;