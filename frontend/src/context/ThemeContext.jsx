
import { createContext } from 'react';

// Creamos el contexto con valores por defecto
export const ThemeContext = createContext({
  darkMode: false,
  toggleDarkMode: () => {}
});