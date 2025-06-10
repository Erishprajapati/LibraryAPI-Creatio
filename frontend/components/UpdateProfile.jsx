import React, { useState } from 'react';
import { API_BASE_URL } from '../src/config.js';

const UpdateProfile = ({ userData, onUpdateSuccess, onNavigate }) => {
  const [formData, setFormData] = useState({
    name: userData?.user || '',
    email: userData?.email || ''
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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
      console.log('Updating profile with data:', formData);
      
      const response = await fetch(`${API_BASE_URL}/user/update-profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      console.log('Response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        setMessage('Profile updated successfully!');
        console.log('Profile updated successfully:', data);
        
        // Show success message for 2 seconds, then navigate to home
        setTimeout(() => {
          onUpdateSuccess(data);
          onNavigate('home');
        }, 2000);
      } else {
        const errorData = await response.json();
        console.error('Profile update failed:', errorData);
        
        // Handle validation errors properly
        if (errorData.detail && Array.isArray(errorData.detail)) {
          // Pydantic validation errors
          const errorMessages = errorData.detail.map(err => err.msg).join(', ');
          setMessage(`Validation error: ${errorMessages}`);
        } else if (errorData.detail) {
          // Single error message
          setMessage(errorData.detail);
        } else {
          setMessage(`Update failed with status: ${response.status}`);
        }
      }
    } catch (err) {
      console.error('Network error:', err);
      setMessage('Network error: Unable to connect to the server.');
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
              <h2 className="card-title text-center mb-4">Update Profile</h2>
              {message && (
                <div className={`alert ${message.includes('successfully') ? 'alert-success' : 'alert-danger'}`}>
                  {message}
                </div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Name</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    name="name" 
                    value={formData.name}
                    onChange={handleChange}
                    required 
                    disabled={isLoading}
                    placeholder="Enter your name"
                  />
                </div>
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
                <div className="d-grid gap-2">
                  <button 
                    className="btn btn-primary" 
                    type="submit" 
                    disabled={isLoading}
                  >
                    {isLoading ? 'Updating...' : 'Update Profile'}
                  </button>
                  <button 
                    type="button"
                    className="btn btn-secondary" 
                    onClick={() => onNavigate('home')}
                    disabled={isLoading}
                  >
                    Cancel
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

export default UpdateProfile; 