import api from './axios'
export const plantsApi = {
  list:   (params)   => api.get('/plants/',        { params }).then(r => r.data),
  get:    (id)       => api.get(`/plants/${id}`).then(r => r.data),
  create: (data)     => api.post('/plants/', data).then(r => r.data),
  update: (id, data) => api.put(`/plants/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/plants/${id}`),
}
