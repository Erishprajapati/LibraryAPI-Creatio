// Configuration for API URLs
const config = {
  // Development environment
  development: {
    apiUrl: 'http://localhost:8000'
  },
  // Production environment - you'll update this with your deployed backend URL
  production: {
    apiUrl: 'https://your-backend-url.railway.app' // Update this with your actual backend URL
  }
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Export the appropriate config
export const API_BASE_URL = config[environment]?.apiUrl || config.development.apiUrl; 