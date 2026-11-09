from contextlib import asynccontextmanager, contextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import get_connection, initialise_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield


app = FastAPI(title="Raj's Practical API", lifespan=lifespan)


@contextmanager
def database_connection():
    connection = get_connection()
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def task_response(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
    }


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool = False


@app.get("/")
def home():
    return {"message": "Hello Raj! Your API is running."}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}! Welcome to my API."}


@app.get("/greet")
def greet(name: str = "Raj"):
    return {"message": f"Hello {name}!"}


@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}


@app.get("/tasks")
def get_tasks():
    with database_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()
        return [task_response(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with database_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return task_response(row)


@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    with database_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (new_task.title, int(new_task.completed)),
        )
        return {
            "id": cursor.lastrowid,
            "title": new_task.title,
            "completed": new_task.completed,
        }


@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    with database_connection() as connection:
        cursor = connection.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return task_response(row)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with database_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")

        connection.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        return {"message": "Task deleted", "task": task_response(row)}