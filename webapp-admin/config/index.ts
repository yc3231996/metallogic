const config = {
  apiBaseUrl: process.env.API_BASE_URL || 'http://127.0.0.1:5000',
  apiKey: process.env.API_KEY || 'p2QtZ91ujRN2db0OyVWPXmvmv7e9zQLBswOiL4REZcY',
  publicApiBaseUrl: '/api',
  auth: {
    username: process.env.AUTH_USERNAME || 'admin',
    password: process.env.AUTH_PASSWORD || 'admin'
  }
};

export default config;