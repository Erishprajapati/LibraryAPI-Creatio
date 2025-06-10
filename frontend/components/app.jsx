import React, { useState, useEffect } from 'react';
import Register from './register.jsx';
import Login from './login.jsx';
import Home from './Home.jsx';
import UpdateProfile from './UpdateProfile.jsx';
import SavedBooks from './SavedBooks.jsx';
import Navbar from './Navbar.jsx';

function App() {
  const [activeTab, setActiveTab] = useState('login');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [currentPage, setCurrentPage] = useState('login');
  const [successMessage, setSuccessMessage] = useState('');

  // Load user data from localStorage on component mount
  useEffect(() => {
    const savedUserData = localStorage.getItem('userData');
    const savedCurrentPage = localStorage.getItem('currentPage');
    
    if (savedUserData) {
      try {
        const parsedUserData = JSON.parse(savedUserData);
        setUserData(parsedUserData);
        setIsLoggedIn(true);
        setCurrentPage(savedCurrentPage || 'home');
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('userData');
        localStorage.removeItem('currentPage');
      }
    }
  }, []);

  const handleLoginSuccess = (data) => {
    setIsLoggedIn(true);
    setUserData(data);
    setCurrentPage('home');
    
    // Save to localStorage
    localStorage.setItem('userData', JSON.stringify(data));
    localStorage.setItem('currentPage', 'home');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserData(null);
    setCurrentPage('login');
    
    // Clear localStorage
    localStorage.removeItem('userData');
    localStorage.removeItem('currentPage');
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
    // Save current page to localStorage
    localStorage.setItem('currentPage', page);
  };

  const handleProfileUpdate = (updatedData) => {
    setUserData(updatedData);
    // Update localStorage with new user data
    localStorage.setItem('userData', JSON.stringify(updatedData));
  };

  const handleRegistrationSuccess = () => {
    setSuccessMessage('Registration successful! Please login with your credentials.');
    setActiveTab('login');
    // Clear success message after 5 seconds
    setTimeout(() => setSuccessMessage(''), 5000);
  };

  // If user is logged in, show the main application with navbar
  if (isLoggedIn && userData) {
    return (
      <div className="App">
        <Navbar 
          userData={userData} 
          onLogout={handleLogout} 
          onNavigate={handleNavigate} 
        />
        
        {currentPage === 'home' && (
          <Home userData={userData} />
        )}
        
        {currentPage === 'saved' && (
          <SavedBooks userData={userData} />
        )}
        
        {currentPage === 'profile' && (
          <UpdateProfile 
            userData={userData} 
            onUpdateSuccess={handleProfileUpdate}
            onNavigate={handleNavigate}
          />
        )}
      </div>
    );
  }

  // If user is not logged in, show login/register tabs
  return (
    <div className="App">
      <div className="container mt-4">
        {successMessage && (
          <div className="alert alert-success alert-dismissible fade show" role="alert">
            {successMessage}
            <button type="button" className="btn-close" onClick={() => setSuccessMessage('')}></button>
          </div>
        )}
        
        <ul className="nav nav-tabs mb-4">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'login' ? 'active' : ''}`}
              onClick={() => setActiveTab('login')}
            >
              Login
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'register' ? 'active' : ''}`}
              onClick={() => setActiveTab('register')}
            >
              Register
            </button>
          </li>
        </ul>
        
        {activeTab === 'login' ? (
          <Login onLoginSuccess={handleLoginSuccess} />
        ) : (
          <Register onRegistrationSuccess={handleRegistrationSuccess} />
        )}
      </div>
    </div>
  );
}

export default App;
