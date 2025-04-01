// File: src/pages/LoginPage.js
import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import EmailForm from '../components/EmailForm';
import OTPVerification from '../components/OTPVerification';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [step, setStep] = useState('email'); // 'email' or 'otp'
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  
  const { initiateEmailLogin, verifyOTP, isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleEmailSubmit = async (email) => {
    setError('');
    setSuccessMessage('');
    
    const result = await initiateEmailLogin(email);
    
    if (result.success) {
      setEmail(email);
      setSuccessMessage('Verification code sent to your email');
      setStep('otp');
    } else {
      setError(result.message);
    }
  };

  const handleOTPSubmit = async (otp) => {
    setError('');
    
    const result = await verifyOTP(email, otp);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.message);
    }
  };

  const handleBackToEmail = () => {
    setStep('email');
    setError('');
    setSuccessMessage('');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {step === 'email' ? 'Sign in to your account' : 'Enter verification code'}
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {error && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
              <div className="flex">
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}
          
          {successMessage && (
            <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
              <div className="flex">
                <div className="ml-3">
                  <p className="text-sm text-green-700">{successMessage}</p>
                </div>
              </div>
            </div>
          )}
          
          {step === 'email' ? (
            <EmailForm onSubmit={handleEmailSubmit} />
          ) : (
            <OTPVerification 
              onSubmit={handleOTPSubmit} 
              onBack={handleBackToEmail}
              email={email}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;