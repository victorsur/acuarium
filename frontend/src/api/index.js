import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

// Aquarium Types
export const aquariumTypes = {
  getAll: () => api.get('/aquarium-types/'),
  getOne: (id) => api.get(`/aquarium-types/${id}/`),
  create: (data) => api.post('/aquarium-types/', data),
  update: (id, data) => api.put(`/aquarium-types/${id}/`, data),
  remove: (id) => api.delete(`/aquarium-types/${id}/`)
}

// Aquariums
export const aquariums = {
  getAll: () => api.get('/aquariums/'),
  getOne: (id) => api.get(`/aquariums/${id}/`),
  create: (data) => api.post('/aquariums/', data),
  update: (id, data) => api.put(`/aquariums/${id}/`, data),
  remove: (id) => api.delete(`/aquariums/${id}/`)
}

// Fish
export const fish = {
  getAll: (aquariumId) =>
    api.get('/fish/', { params: aquariumId ? { aquarium: aquariumId } : {} }),
  getOne: (id) => api.get(`/fish/${id}/`),
  create: (data) => api.post('/fish/', data),
  update: (id, data) => api.put(`/fish/${id}/`, data),
  remove: (id) => api.delete(`/fish/${id}/`)
}

// Plants
export const plants = {
  getAll: (aquariumId) =>
    api.get('/plants/', { params: aquariumId ? { aquarium: aquariumId } : {} }),
  getOne: (id) => api.get(`/plants/${id}/`),
  create: (data) => api.post('/plants/', data),
  update: (id, data) => api.put(`/plants/${id}/`, data),
  remove: (id) => api.delete(`/plants/${id}/`)
}

// Lighting
export const lighting = {
  getAll: (aquariumId) =>
    api.get('/lighting/', { params: aquariumId ? { aquarium: aquariumId } : {} }),
  getOne: (id) => api.get(`/lighting/${id}/`),
  create: (data) => api.post('/lighting/', data),
  update: (id, data) => api.put(`/lighting/${id}/`, data),
  remove: (id) => api.delete(`/lighting/${id}/`)
}

// Maintenance Tasks
export const maintenanceTasks = {
  getAll: (aquariumId, isCompleted) => {
    const params = {}
    if (aquariumId) params.aquarium = aquariumId
    if (isCompleted !== undefined && isCompleted !== null)
      params.is_completed = isCompleted
    return api.get('/maintenance-tasks/', { params })
  },
  getOne: (id) => api.get(`/maintenance-tasks/${id}/`),
  create: (data) => api.post('/maintenance-tasks/', data),
  update: (id, data) => api.put(`/maintenance-tasks/${id}/`, data),
  remove: (id) => api.delete(`/maintenance-tasks/${id}/`),
  complete: (id) => api.post(`/maintenance-tasks/${id}/complete/`)
}

export default api
