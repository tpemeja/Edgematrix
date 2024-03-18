# FastAPI Device Management Project

This project is a FastAPI-based application for managing devices.
It provides endpoints for creating, reading, updating, and deleting device information, as well as running tests inside a Docker container.

## Features
- **CRUD Operations:** Create, read, update, and delete device information via API endpoints.
- **Validation:** Input data is validated using Pydantic models to ensure data integrity.
- **Database:** Utilizes SQLite for storing device information.
- **Testing:** Includes **pytest** tests to ensure the functionality of the API endpoints.
- **Linting:** Uses **pylint** for code linting to maintain code quality.

## Installation
### Clone the repository:

```bash
git clone <repository_url>
```

## Usage - Docker Container
### Creating the Docker Image
To create the Docker image, execute:

```bash
docker build -t myapp .
```

### Running the Docker Container
To run the Docker container, execute:

```bash
docker run -d -p <PORT>:80 -v <DATABASE_PATH>:/data myapp
```

* **\<PORT>** is the port number to map the FastAPI server to. For example, **8000**.
* **\<DATABASE_PATH>** is the path to the directory where to store the SQLite database file. For example, **/home/user/myproject/database**.

### Accessing the Swagger UI
Once the Docker container is running, you can access the Swagger UI by navigating to:

```bash
http://localhost:<PORT>/docs
```
### Running Tests
To run tests using pytest inside a Docker container, execute:
```bash
docker run -v <DATABASE_PATH>:/data myapp pytest
```

Or to run it on an existing container
```bash
docker exec <CONTAINER_NAME|CONTAINER_ID> pytest
```

### Running Linting
To perform linting using pylint, run:

```bash
docker run myapp pylint /code/app
```

Or to run it on an existing container
```bash
docker exec <CONTAINER_NAME|CONTAINER_ID> pylint /code/app
```

## Usage - Local Testing
### Installing Requirements
First, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Running Tests Locally
To run tests locally using pytest, execute:

```bash
pytest
```

### Running Linting Locally
To perform linting using pylint locally, run:

```bash
pylint app/
```

### Starting the FastAPI Server Locally
To start the FastAPI server locally, execute:

```bash
uvicorn app.main:app --host 0.0.0.0 --port <PORT>
```

### Accessing the Swagger UI
Once the FastAPI server is running locally, you can access the Swagger UI by navigating to:

```bash
http://localhost:<PORT>/docs
```

The database will be stored in **/data/devices.db** by default
unless the value is modified using the variable **DATABASE_PATH** in the *app/database/startup.py* file.