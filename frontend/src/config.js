// Configuration for API URLs
// Updated for Render deployment - CORS fix applied
const config = {
  // Development environment
  development: {
    apiUrl: 'http://localhost:8000'
  },
  // Production environment - updated with your deployed backend URL
  production: {
    apiUrl: 'https://libraryapi-creatio.onrender.com'
  }
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Export the appropriate config
export const API_BASE_URL = config[environment]?.apiUrl || config.development.apiUrl; 