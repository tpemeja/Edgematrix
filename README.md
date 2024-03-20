# FastAPI Device Management Project

This project is a FastAPI-based application for managing devices.
It provides endpoints for creating, reading, updating, and deleting device information, as well as running tests inside a Docker container.

---

## Features
- **CRUD Operations:** Create, read, update, and delete device information via API endpoints.
- **Validation:** Input data is validated using **Pydantic** models to ensure data integrity.
- **Database:** Utilizes **SQLite** for storing device information.
- **Testing:** Includes **pytest** tests to ensure the functionality of the API endpoints.
- **Linting:** Uses **pylint** for code linting to maintain code quality.

---

## Project Structure
```
.
├── Dockerfile
├── README.md
├── COMMENTS.md
├── requirements.txt
├── .gitignore
└── app/
    ├── main.py
    ├── api/
    │   └── routers/
    │       └── devices.py
    ├── database/
    │   └── operations/
    │       └── devices.py
    ├── models/
    │   ├── coordinate.py
    │   └── device.py
    └── tests/
        └── unit/
            └── test_device_api.py
└── images/
    ├── jwt_authentication.svg
    └── oauth2.0_authentication.svg
```

---
## Installation
### Clone the repository:

```bash
git clone https://github.com/tpemeja/Edgematrix-Private
```

---

## Usage - Docker Container
### Getting the Docker Image
For the rest of the project, we will assume that you have built the image locally with the name **myapp**.
To obtain the Docker image, you have two options:

#### Build the Image Locally:
You can create the Docker image by executing the following command in the directory containing your Dockerfile:
```bash
docker build -t myapp .
```
This command will build the Docker image with the tag **myapp**.

#### Download from Docker Hub:
Alternatively, you can directly download the pre-built image from Docker Hub using the following command:

```bash
docker pull tpemeja/edgematrix:main-latest
```
This command will pull the latest version of the image tagged as main-latest from the [Docker Hub repository](https://hub.docker.com/repository/docker/tpemeja/edgematrix) *tpemeja/edgematrix*.


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

---

## Usage - Local Testing
### Installing Requirements
First, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Creating Database Directory
Ensure you have created a directory for the SQLite database. You can create it using the following command:

```bash
mkdir /data
```

The database will be stored in **/data/devices.db** by default
unless the value is modified using the variable **DATABASE_PATH** in the *app/database/startup.py* file.

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
