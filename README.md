# Encodex

Encodex is an API built with Python's FastAPI framework. It provides a robust and flexible solution for creating, managing, and using custom encoding standards.

With Encodex, you can define your own encoding standards, apply them to encode and decode data, and store and retrieve them from a MySQL database. This makes Encodex a practical tool for managing encoding standards in software development projects.

## Overview
![API routes](./routes.png)
## Installation
Docker is required to run the project.
```bash
# Clone the repository
git clone https://github.com/MathisJANKOVIC/Encodex.git

# Go to the project directory and setup docker services
docker-compose up

# Enter the FastAPI container
docker exec -it encodex-fastapi bash

# Run the database models
python src/database/models.py