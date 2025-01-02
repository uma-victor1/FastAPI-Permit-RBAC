<!-- todo -->
<!-- add image to this header -->
<p align="center">
  <a href=""><img src="" alt="FastAPI+permit"></a>
</p>
<p align="center">
    <em>Build a Secure Contact Management App with FastAPI and Permit RBAC: A Step-by-Step Guide</em>
</p>
<!-- todo -->

# FastAPI+Permit

A secure contact management app built with FastAPI and Permit RBAC.

## Technologies Used

This project is developed using the following technologies:

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **Uvicorn:** A lightning-fast ASGI server, used to run FastAPI application.
- **PyMySQL:** A pure-Python MySQL/MariaDB client library.
- **SQLAlchemy:** A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Alembic:** A database migration tool for SQLAlchemy.

## Project Structure

The project structure is organized as follows:

- **controllers:** Contains the controllers responsible for handling requests and business logic.
- **db:** Contains the database driver and logic for create database and working with tables.
- **middlewares:** Houses various middleware for request handling (e.g., static files, CORS).
- **models:** Stores the application's data models and schemas.
- **services:** Implements business logic for working with objects.
- **static:** Contaim static files (Some js library, css, images, etc.).
- **templates:** Holds HTML templates for rendering views.
- **utils:** Contains utility functions.

```
├── app
│   ├── constants.py
│   ├── controllers
│   │   ├── auth_controller.py
│   │   ├── page_controller.py
│   │   └── user_controller.py
│   ├── db
│   │   ├── context.py
│   │   └── user_db.py
│   ├── db_init.bash
│   ├── db_init.py
│   ├── dev.bash
│   ├── main.py
│   ├── middlewares
│   │   ├── cors_middleware.py
│   │   └── static_middleware.py
│   ├── models
│   │   ├── db.py
│   │   ├── dto.py
│   ├── prod.sh
│   ├── services
│   │   ├── jwt_service.py
│   │   └── user_service.py
│   ├── static
│   ├── templates
│   │   └── main.jinja
│   └── utils
│       ├── background_schedule_task.py
│       ├── bcrypt_hashing.py
│       ├── dependencies.py
│       ├── formating.py
│       ├── lifespan.py
│       └── sha256_hashing.py
├── docker-compose.yml
├── Dockerfile
├── install_env.sh
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone project
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To start the FastAPI application, use the following command:

```bash
cd app
bash dev.bash
```

## Deploying the Project

```sh
docker compose up -d
```
