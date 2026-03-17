import api from './axios'
export const fishApi = {
  list:   (params)   => api.get('/fish/',        { params }).then(r => r.data),
  get:    (id)       => api.get(`/fish/${id}`).then(r => r.data),
  create: (data)     => api.post('/fish/', data).then(r => r.data),
  update: (id, data) => api.put(`/fish/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/fish/${id}`),
}
