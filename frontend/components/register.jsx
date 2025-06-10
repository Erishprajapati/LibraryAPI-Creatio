import React, { useState } from 'react';

const Register = ({ onRegistrationSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setIsLoading(true);

    try {
      console.log('Sending registration request with data:', formData);
      
      const response = await fetch('http://localhost:8000/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (response.ok) {
        const data = await response.json();
        setMessage('User registered successfully!');
        console.log('Registration successful:', data);
        // Clear form after successful registration
        setFormData({
          name: '',
          email: '',
          password: ''
        });
        
        // Call the success callback to navigate to login
        if (onRegistrationSuccess) {
          onRegistrationSuccess();
        }
      } else {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
        setMessage(errorData.detail || `Registration failed with status: ${response.status}`);
      }
    } catch (err) {
      console.error('Network error:', err);
      setMessage('Network error: Unable to connect to the server. Please check if the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Register</h2>
      {message && (
        <div className={`alert ${message.includes('successfully') ? 'alert-success' : 'alert-danger'}`}>
          {message}
        </div>
      )}
      <form onSubmit={handleSubmit} className="mt-3">
        <div className="mb-3">
          <label>Name</label>
          <input 
            type="text" 
            className="form-control" 
            name="name" 
            value={formData.name}
            onChange={handleChange}
            required 
            disabled={isLoading}
          />
        </div>
        <div className="mb-3">
          <label>Email</label>
          <input 
            type="email" 
            className="form-control" 
            name="email" 
            value={formData.email}
            onChange={handleChange}
            required 
            disabled={isLoading}
          />
        </div>
        <div className="mb-3">
          <label>Password</label>
          <div className="input-group">
            <input 
              type={showPassword ? "text" : "password"}
              className="form-control" 
              name="password" 
              value={formData.password}
              onChange={handleChange}
              required 
              disabled={isLoading}
            />
            <button 
              type="button" 
              className="btn btn-outline-secondary" 
              onClick={togglePasswordVisibility}
              disabled={isLoading}
            >
              {showPassword ? "🙈" : "👁️"}
            </button>
          </div>
        </div>
        <button 
          className="btn btn-primary" 
          type="submit" 
          disabled={isLoading}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default Register;
