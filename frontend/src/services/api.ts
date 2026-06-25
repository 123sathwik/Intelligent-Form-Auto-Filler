import axios from 'axios'

const baseURL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${
  import.meta.env.VITE_API_V1_PREFIX || '/api/v1'
}`

const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
})

// Request interceptor to automatically attach authorization tokens
apiClient.interceptors.request.use(
  (config) => {
    // Stash token fetching logic from auth providers if needed
    // const token = localStorage.getItem('auth_token')
    // if (token && config.headers) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for unified response formatting
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const customError = {
      message: error.response?.data?.detail || 'An unexpected server error occurred',
      status: error.response?.status || 500,
    }
    return Promise.reject(customError)
  }
)

export default apiClient
