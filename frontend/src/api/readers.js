import request from './request'

// 读者相关的接口
export function listReaders() {
  return request.get('/readers')
}

export function searchReaders(keyword) {
  return request.get('/readers/search', { params: { keyword } })
}

export function getReader(id) {
  return request.get(`/readers/${id}`)
}

export function createReader(data) {
  return request.post('/readers', data)
}

export function updateReader(id, data) {
  return request.put(`/readers/${id}`, data)
}

export function deleteReader(id) {
  return request.delete(`/readers/${id}`)
}
