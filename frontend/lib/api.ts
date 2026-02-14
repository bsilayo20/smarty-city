/**
 * API client for Smart City FIS backend
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface Resource {
  id: string
  name: string
  type: string
  latitude: number
  longitude: number
  location?: string
  capacity?: number
  currentLevel?: number
  population?: number
  status?: string
  description?: string
  lastUpdated?: string
}

export const resourcesApi = {
  /**
   * Get all resources
   */
  getAll: async (type?: string): Promise<Resource[]> => {
    const params = type && type !== 'all' ? { type } : {}
    const response = await apiClient.get('/api/v1/resources', { params })
    return response.data
  },

  /**
   * Get resource by ID
   */
  getById: async (id: string): Promise<Resource> => {
    const response = await apiClient.get(`/api/v1/resources/${id}`)
    return response.data
  },

  /**
   * Get resources by location
   */
  getByLocation: async (
    latitude: number,
    longitude: number,
    radius: number = 10
  ): Promise<Resource[]> => {
    const response = await apiClient.get('/api/v1/resources/nearby', {
      params: { latitude, longitude, radius },
    })
    return response.data
  },
}

export const dataIngestionApi = {
  /**
   * List all data sources
   */
  listSources: async () => {
    const response = await apiClient.get('/api/v1/ingestion/sources')
    return response.data
  },

  /**
   * Trigger data ingestion
   */
  triggerIngestion: async (sourceId?: string, sourceType?: string) => {
    const response = await apiClient.post('/api/v1/ingestion/fetch', {
      source_id: sourceId,
      source_type: sourceType,
    })
    return response.data
  },

  /**
   * Get ingestion status
   */
  getStatus: async () => {
    const response = await apiClient.get('/api/v1/ingestion/status')
    return response.data
  },
}

export const analyticsApi = {
  /**
   * Get resource statistics
   */
  getStats: async () => {
    const response = await apiClient.get('/api/v1/analytics/stats')
    return response.data
  },

  /**
   * Get resource distribution by type
   */
  getDistribution: async (type?: string) => {
    const params = type ? { type } : {}
    const response = await apiClient.get('/api/v1/analytics/distribution', {
      params,
    })
    return response.data
  },
}

export default apiClient
