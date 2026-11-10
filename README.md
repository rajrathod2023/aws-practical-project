# Task Tracker API

A local learning project built with FastAPI, SQLite, Docker and Docker Compose.

## Features

- Create, list, complete and delete tasks
- Validate task titles
- Return 404 for missing tasks
- Store tasks in SQLite
- Preserve the database using a Docker volume
- Explore endpoints through interactive API documentation

## Requirements

- Docker Desktop running with Linux containers
- Docker Compose

## Run the application

From the project folder, create the database volume:

```powershell
docker volume create raj-task-data
```

Start the API:

```powershell
docker compose up -d --build
```

Open:

- API documentation: http://127.0.0.1:8001/docs
- Health check: http://127.0.0.1:8001/health
- Tasks: http://127.0.0.1:8001/tasks

## API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Check API availability |
| GET | /tasks | List tasks |
| GET | /tasks/{task_id} | Retrieve one task |
| POST | /tasks | Create a task |
| PATCH | /tasks/{task_id}/complete | Mark a task complete |
| DELETE | /tasks/{task_id} | Delete a task |

Example request body for POST /tasks:

```json
{
  "title": "Learn Docker Compose",
  "completed": false
}
```

## View logs

```powershell
docker compose logs --tail 20 api
```

## Stop the application

```powershell
docker compose down
```

The external volume `raj-task-data` remains after containers are removed.
It stores the SQLite database at `/app/data/tasks.db` inside the container.

## Project files

- main.py — API endpoints and database operations
- database.py — database connection and table creation
- requirements.txt — Python dependencies
- Dockerfile — image build instructions
- compose.yaml — service, port and volume configuration
- .dockerignore — files excluded from Docker builds
- .gitignore — files excluded from Git commits

## Current limitations

This is a learning project running locally. It has no authentication and has
not been deployed to AWS. The database volume provides persistence, but
backups are not yet configured.

## Automated tests

Install the development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Run the tests:

```powershell
python -m pytest -v
```

Tests use temporary SQLite databases, keeping saved application tasks separate.
GitHub Actions runs the tests on pushes to main and pull requests targeting main.

## Continuous integration checks

GitHub Actions runs these checks for pushes to main and pull requests targeting main:

1. Run five automated API tests using isolated SQLite databases.
2. Build the Docker image.
3. Start a test container.
4. Wait for the API to become ready and check the /health endpoint.
5. Display container logs and remove the test container.

This workflow validates the application. It does not deploy it.

## Database backups (PowerShell)

With the API container running, run:

```powershell
.\backup.ps1
```

The script saves a dated SQLite backup in `backups/`.
This folder is excluded from Git and Docker builds.
Backups remain on your PC; keep a separate copy for protection against disk failure.