import api from './axios'
export const maintenanceApi = {
  list:   (params)   => api.get('/maintenance/',        { params }).then(r => r.data),
  get:    (id)       => api.get(`/maintenance/${id}`).then(r => r.data),
  create: (data)     => api.post('/maintenance/', data).then(r => r.data),
  update: (id, data) => api.put(`/maintenance/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/maintenance/${id}`),
}
