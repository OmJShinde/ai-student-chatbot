# AI Student Query Chatbot

A production-ready AI chatbot using FastAPI, Sentence Transformers, and MongoDB (with local JSON fallback).

## Project Structure
- `app/`: Backend FastAPI application
- `static/`: Frontend HTML/JS/CSS
- `tests/`: Automated tests
- `docker-compose.yml`: Container orchestration

## Setup

### Prerequisites
- Python 3.9+
- Docker (optional)

### Local Development (No Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest httpx
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
   The app uses a local JSON database by default (`data/db.json`).

3. Access the Chatbot:
   Open [http://localhost:8000](http://localhost:8000)

4. Access Admin Panel:
   Open [http://localhost:8000/admin](http://localhost:8000/admin)
   - **Username**: admin
   - **Password**: admin123

### Docker
1. Build and run:
   ```bash
   docker-compose up --build
   ```
   This starts the App and a MongoDB instance.

## Testing
Run automated tests:
```bash
python -m pytest
```
