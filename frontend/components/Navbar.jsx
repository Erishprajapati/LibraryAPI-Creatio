import React, { useState } from 'react';

const Navbar = ({ userData, onLogout, onNavigate }) => {
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  const handleLogoutClick = () => {
    setShowLogoutModal(true);
  };

  const handleLogoutConfirm = () => {
    setShowLogoutModal(false);
    onLogout();
  };

  const handleLogoutCancel = () => {
    setShowLogoutModal(false);
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <a className="navbar-brand" href="#" onClick={() => onNavigate('home')}>
            📚 Library System
          </a>
          
          <div className="navbar-nav ms-auto">
            <button 
              className="nav-link btn btn-link text-white" 
              onClick={() => onNavigate('home')}
            >
              Home
            </button>
            <button 
              className="nav-link btn btn-link text-white" 
              onClick={() => onNavigate('saved')}
            >
              Saved Books
            </button>
            <button 
              className="nav-link btn btn-link text-white" 
              onClick={() => onNavigate('profile')}
            >
              Update Profile
            </button>
            <button 
              className="nav-link btn btn-link text-white" 
              onClick={handleLogoutClick}
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Logout Confirmation Modal */}
      {showLogoutModal && (
        <div className="modal fade show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirm Logout</h5>
                <button type="button" className="btn-close" onClick={handleLogoutCancel}></button>
              </div>
              <div className="modal-body">
                <p>Are you sure you want to logout?</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleLogoutCancel}>
                  No, Stay
                </button>
                <button type="button" className="btn btn-primary" onClick={handleLogoutConfirm}>
                  Yes, Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar; 