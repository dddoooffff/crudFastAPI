from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()


books = [
    {"id": 1, "title": "Backend Разработка на Python"},
    {"id": 2, "title": "Frontend разработка"}
]


@app.get("/", tags=["Книги"])
async def get_all():
    return books

@app.get("/book/{book_id}", tags=["Книга"])
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена!")


class NewBook(BaseModel):
    title: str

@app.post("/books")
async def create_book(title: str):
    books.append({
        "id": len(books) + 1,
        "title": title,
    })
    return {"success": True, "message": "Книга успешно добавлена!"}

@app.put("/book/{book_id}")
async def update_book(book_id: int, title: str):
    for book in books:
        if book["id"] == book_id:
            if title:
                book.update({"title": title})

@app.delete("/book/{book_id}")
async def delete_book(book_id: int):
    global books
    books = [book for book in books if book["id"] != book_id]  # Удаляем книгу
    for idx, book in enumerate(books):
        book["id"] = idx + 1  # Обновляем индексы
        print(book["id"], " ", idx)

        return {"success": True, "message": "Книга успешно удалена!"}


    raise HTTPException(status_code=404, detail="Не удалось удалить книгу")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)