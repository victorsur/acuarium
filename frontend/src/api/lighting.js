import api from './axios'
export const lightingApi = {
  list:   (params)   => api.get('/lighting/',        { params }).then(r => r.data),
  get:    (id)       => api.get(`/lighting/${id}`).then(r => r.data),
  create: (data)     => api.post('/lighting/', data).then(r => r.data),
  update: (id, data) => api.put(`/lighting/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/lighting/${id}`),
}
