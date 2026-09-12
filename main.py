from fastapi import FastAPI
from init_db import init_db
from routers import books, readers, borrows, auth, me

app = FastAPI()
init_db()  # 建表 + 迁移 + 生成默认管理员

app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrows.router)
app.include_router(auth.router)
app.include_router(me.router)
