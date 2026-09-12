import request from './request'

// 借阅相关的接口
export function listBorrows(params) {
  return request.get('/borrows', { params })
}

// 借书:传入图书 id 和读者 id
export function borrowBook(bookId, readerId) {
  return request.post('/borrow', { book_id: bookId, reader_id: readerId })
}

// 还书:传入借阅记录 id
export function returnBook(id) {
  return request.post(`/borrows/${id}/return`)
}
