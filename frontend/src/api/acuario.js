import api from './axios'
export const acuarioApi = {
  list:   (params)   => api.get('/acuario/',        { params }).then(r => r.data),
  get:    (id)       => api.get(`/acuario/${id}`).then(r => r.data),
  create: (data)     => api.post('/acuario/', data).then(r => r.data),
  update: (id, data) => api.put(`/acuario/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/acuario/${id}`),
}
