# FastAPI REST Application with SQLModel

This is a REST API for managing PostgreSQL server configuration using SQLModel for database interactions.

## Setup

1. Install uv (if not already installed):

   ```bash
   pip install uv
   ```

2. Create a virtual environment:

   ```bash
   uv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On Unix/macOS:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   uv pip install -e .
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

To run the tests:

   ```bash
   pytest
   ```

## API Endpoints

- `GET /health` : Health check endpoint
- `POST /servers/` : Create a new PostgreSQL server configuration
- `GET /servers/` : Get all configured PostgreSQL servers
- `GET /servers/{server_id}` : Get a specific PostgreSQL server configuration
- `PUT /servers/{server_id}` : Update a PostgreSQL server configuration
- `DELETE /servers/{server_id}` : Delete a PostgreSQL server configuration