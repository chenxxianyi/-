import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

type DataRequest = Omit<AxiosInstance, 'get' | 'delete' | 'post' | 'put' | 'patch'> & {
  get<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T>
  delete<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T>
  post<T = unknown, D = unknown>(url: string, data?: D, config?: AxiosRequestConfig<D>): Promise<T>
  put<T = unknown, D = unknown>(url: string, data?: D, config?: AxiosRequestConfig<D>): Promise<T>
  patch<T = unknown, D = unknown>(url: string, data?: D, config?: AxiosRequestConfig<D>): Promise<T>
}

const http = axios.create({
  baseURL: '/api',
  timeout: 12000,
})

http.interceptors.request.use((config) => {
  const token = window.localStorage.getItem('kr_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：解包后端统一响应格式 { code, message, data }
http.interceptors.response.use(
  (response) => {
    const body = response.data
    // 后端返回统一格式 { code, message, data }
    if (body && typeof body === 'object' && 'code' in body) {
      if (body.code === 0) {
        return body.data
      }
      return Promise.reject(new Error(body.message || '请求失败'))
    }
    // 非统一格式（如文件流），原样返回
    return body
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '网络错误'
    return Promise.reject(new Error(message))
  },
)

export const request = http as DataRequest
