// File: src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in by verifying token
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          // Configure axios to use token
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Fetch user details
          const response = await axios.get('/api/user-details');
          setUser(response.data);
        } catch (error) {
          // If token is invalid, remove it
          console.error('Authentication error:', error);
          localStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
        }
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []);

  // Login with email
  const initiateEmailLogin = async (email) => {
    try {
      const response = await axios.post('/api/register', { email });
      return { success: true, message: response.data.message };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'An error occurred during login initialization'
      };
    }
  };

  // Verify OTP
  const verifyOTP = async (email, otp) => {
    try {
      // This would ideally be a separate endpoint, but we're using what's available
      // In a real app, you'd have a dedicated endpoint for OTP verification
      const response = await axios.post('/api/token/', { 
        email: email,
        one_time_password: otp
      });
      
      // Store token in localStorage
      localStorage.setItem('token', response.data.access);
      
      // Set auth header for future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      
      // Fetch user details
      const userResponse = await axios.get('/api/user-details');
      setUser(userResponse.data);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Invalid verification code'
      };
    }
  };

  // Logout user
  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      loading,
      initiateEmailLogin,
      verifyOTP,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;