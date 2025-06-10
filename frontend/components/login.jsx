import React, { useState } from 'react';

const Login = ({ onLoginSuccess }) => {
  const [formData, setFormData] = useState({
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
      console.log('Sending login request with data:', formData);
      
      const response = await fetch('http://localhost:8000/home/login', {
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
        setMessage('Login successful!');
        console.log('Login successful:', data);
        
        // Clear form after successful login
        setFormData({
          email: '',
          password: ''
        });
        
        // Call the parent component's success handler
        onLoginSuccess(data);
      } else {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        
        // Handle different types of error responses
        let errorMessage = 'Login failed';
        if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (Array.isArray(errorData)) {
          errorMessage = errorData.map(err => err.msg || err.message).join(', ');
        } else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
        
        setMessage(errorMessage);
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
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">Login</h2>
              {message && (
                <div className={`alert ${message.includes('successful') ? 'alert-success' : 'alert-danger'}`}>
                  {message}
                </div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input 
                    type="email" 
                    className="form-control" 
                    name="email" 
                    value={formData.email}
                    onChange={handleChange}
                    required 
                    disabled={isLoading}
                    placeholder="Enter your email"
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <div className="input-group">
                    <input 
                      type={showPassword ? "text" : "password"}
                      className="form-control" 
                      name="password" 
                      value={formData.password}
                      onChange={handleChange}
                      required 
                      disabled={isLoading}
                      placeholder="Enter your password"
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
                <div className="d-grid">
                  <button 
                    className="btn btn-primary" 
                    type="submit" 
                    disabled={isLoading}
                  >
                    {isLoading ? 'Logging in...' : 'Login'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;