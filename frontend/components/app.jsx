import React, { useState } from 'react';
import Register from './register.jsx';
import Login from './login.jsx';

function App() {
  const [activeTab, setActiveTab] = useState('login');

  return (
    <div className="App">
      <div className="container mt-4">
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
        
        {activeTab === 'login' ? <Login /> : <Register />}
      </div>
    </div>
  );
}

export default App;
