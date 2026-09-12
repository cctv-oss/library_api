import request from './request'

// 读者自服务接口(读者登录后自己用的)
export function myBorrows() {
  return request.get('/me/borrows')
}

export function myBorrow(bookId) {
  return request.post('/me/borrow', { book_id: bookId })
}

export function myReturn(id) {
  return request.post(`/me/borrows/${id}/return`)
}
