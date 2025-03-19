import React, { createContext, useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if the user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // In a real implementation, this would validate the token with the backend
        const token = localStorage.getItem('token');
        
        if (token) {
          // Simulate API call to get user data
          // In production, this would be a real API call
          setTimeout(() => {
            // Dummy user data for demo purposes
            setUser({
              id: '1',
              name: 'John Doe',
              email: 'john.doe@example.com',
              avatar: 'https://randomuser.me/api/portraits/men/1.jpg'
            });
            setLoading(false);
          }, 1000);
        } else {
          setUser(null);
          setLoading(false);
        }
      } catch (error) {
        console.error('Authentication check failed', error);
        setUser(null);
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setLoading(true);
    
    try {
      // In a real implementation, this would make an API call
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // For demo purposes, accept any credentials
      const userData = {
        id: '1',
        name: 'John Doe',
        email: email,
        avatar: 'https://randomuser.me/api/portraits/men/1.jpg'
      };
      
      // Store token in localStorage (would come from the API in a real app)
      localStorage.setItem('token', 'demo-token');
      
      setUser(userData);
    } catch (error) {
      console.error('Login failed', error);
      throw new Error('Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (name: string, email: string, password: string) => {
    setLoading(true);
    
    try {
      // In a real implementation, this would make an API call
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // For demo purposes, create a user with provided details
      const userData = {
        id: '1',
        name: name,
        email: email,
        avatar: 'https://randomuser.me/api/portraits/men/1.jpg'
      };
      
      // Store token in localStorage (would come from the API in a real app)
      localStorage.setItem('token', 'demo-token');
      
      setUser(userData);
    } catch (error) {
      console.error('Registration failed', error);
      throw new Error('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        loading,
        login,
        register,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
