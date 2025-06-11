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

// Check if we're running on Render (production)
const isDeployed = window.location.hostname.includes('onrender.com') || 
                   window.location.hostname.includes('vercel.app') ||
                   window.location.hostname.includes('netlify.app');

// Get current environment
const environment = isDeployed ? 'production' : (import.meta.env.MODE || 'development');

// Export the appropriate config
export const API_BASE_URL = config[environment]?.apiUrl || config.development.apiUrl; 