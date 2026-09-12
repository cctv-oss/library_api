import request from './request'

// 图书相关的接口都集中写在这里,页面里直接调用这些函数就行
export function listBooks() {
  return request.get('/books')
}

export function getBook(id) {
  return request.get(`/books/${id}`)
}

export function createBook(data) {
  return request.post('/books', data)
}

export function updateBook(id, data) {
  return request.put(`/books/${id}`, data)
}

export function deleteBook(id) {
  return request.delete(`/books/${id}`)
}
