import { request } from '@/utils/request'

export function loginApi(payload: { email: string; password: string }) {
  return request.post('/auth/login', payload)
}

export function registerApi(payload: { username: string; email: string; password: string }) {
  return request.post('/auth/register', payload)
}

export function getMeApi() {
  return request.get('/auth/me')
}
