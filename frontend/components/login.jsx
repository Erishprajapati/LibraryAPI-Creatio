import React, { useState } from 'react';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
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
        setIsLoggedIn(true);
        setUserData(data);
        console.log('Login successful:', data);
        
        // Clear form after successful login
        setFormData({
          email: '',
          password: ''
        });
      } else {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        setMessage(errorData.detail || `Login failed with status: ${response.status}`);
        setIsLoggedIn(false);
        setUserData(null);
      }
    } catch (err) {
      console.error('Network error:', err);
      setMessage('Network error: Unable to connect to the server. Please check if the backend is running.');
      setIsLoggedIn(false);
      setUserData(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserData(null);
    setMessage('');
  };

  if (isLoggedIn && userData) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <div className="card-body text-center">
                <h2 className="card-title text-success">Welcome!</h2>
                <p className="card-text">{userData.message}</p>
                <p className="card-text"><strong>User:</strong> {userData.user}</p>
                <button 
                  className="btn btn-primary" 
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

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
                  <input 
                    type="password" 
                    className="form-control" 
                    name="password" 
                    value={formData.password}
                    onChange={handleChange}
                    required 
                    disabled={isLoading}
                    placeholder="Enter your password"
                  />
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
