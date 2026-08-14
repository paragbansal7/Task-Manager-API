# Task Manager API

A simple in-memory CRUD API built with FastAPI to practice core backend concepts: path parameters, query parameters, request bodies, response models, and dependency injection.

## Features

- Create, read, update, and delete tasks
- Filter tasks by completion status
- Request/response validation via Pydantic models
- Separate input (`TaskCreate`) and output (`TaskResponse`) schemas
- Token-based route protection using FastAPI's dependency injection system

## Tech Stack

- Python 3
- FastAPI
- Pydantic

## Setup

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

## Authentication

All routes require a custom header for a (fake) token check, used here to practice dependency injection:

```
x-token: secret-token
```

Requests without this header, or with the wrong value, receive a `401 Unauthorized`.

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List all tasks (optional `?completed=true/false` filter) |
| GET | `/tasks/{task_id}` | Get a single task by ID |
| PUT | `/tasks/{task_id}` | Update a task by ID |
| DELETE | `/tasks/{task_id}` | Delete a task by ID |

## Example Requests

**Create a task**
```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "x-token: secret-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Dependency Injection", "description": "Practice with FastAPI Depends()", "priority": 1}'
```

**Get all incomplete tasks**
```bash
curl "http://127.0.0.1:8000/tasks?completed=false" \
  -H "x-token: secret-token"
```

**Get a single task**
```bash
curl "http://127.0.0.1:8000/tasks/1" \
  -H "x-token: secret-token"
```

**Update a task**
```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "x-token: secret-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Dependency Injection", "description": "Done", "completed": true, "priority": 1}'
```

**Delete a task**
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1" \
  -H "x-token: secret-token"
```

## Known Limitations

- Data is stored in memory (a Python list) and resets whenever the server restarts — no database yet.
- Authentication is a hardcoded token for practice purposes only, not production-ready.

## What's Next

This project is a checkpoint before adding a real database. The next iteration will swap the in-memory list for SQLite/PostgreSQL via SQLAlchemy, with the DB session itself injected using the same `Depends()` pattern already used here for authentication.
