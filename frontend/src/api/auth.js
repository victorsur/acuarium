import api from './axios'

export const authApi = {
  login:    (username, password) => api.post('/auth/login', { username, password }).then(r => r.data),
  me:       ()                   => api.get('/auth/me').then(r => r.data),
  register: (payload)            => api.post('/auth/register', payload).then(r => r.data),
}

