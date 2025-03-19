import React, { createContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: React.ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Check if user has previously set a theme preference
  const getInitialTheme = (): Theme => {
    // Check if window is defined (for SSR)
    if (typeof window !== 'undefined') {
      // Check local storage
      const storedTheme = localStorage.getItem('theme') as Theme | null;
      if (storedTheme) {
        return storedTheme;
      }

      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      return prefersDark ? 'dark' : 'light';
    }

    // Default to light theme
    return 'light';
  };

  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    // Update localStorage when theme changes
    localStorage.setItem('theme', theme);

    // Update the html class
    const root = window.document.documentElement;
    
    // Remove both classes
    root.classList.remove('light', 'dark');
    // Add the current theme class
    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    toggleTheme,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
