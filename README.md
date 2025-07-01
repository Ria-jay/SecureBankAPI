# SecureBankAPI

SecureBankAPI is a lightweight, secure banking API built with FastAPI. It demonstrates secure API development with features like JWT authentication, rate limiting, role-based access control, containerization, and CI/CD workflows. This project also integrates static analysis tools for automated security scanning.


# Features

- User registration and login with password hashing
- JWT-based authentication for session management
- Role-based access control (user and admin privileges)
- Rate limiting to protect against brute-force attacks
- Protected endpoints using FastAPI dependencies
- OWASP threat modeling using Threat Dragon
- CI/CD pipeline using GitHub Actions
- Security scanning using Semgrep and Snyk
- Docker containerization for deployment


# Technology Stack

- *Framework*: FastAPI
- *Language*: Python 3
- *Authentication*: JWT via `python-jose`
- *Password Hashing*: bcrypt via `passlib`
- *Security Tools*: SlowAPI, Semgrep, Snyk
- *Containerization*: Docker
- *CI/CD*: GitHub Actions
- *Threat Modeling*: OWASP Threat Dragon


# Running Locally with Docker

```bash
git clone https://github.com/Ria-jay/SecureBankAPI.git
cd SecureBankAPI
docker build -t securebankapi .
docker run -d -p 8000:8000 --name securebankapi_container securebankapi

Visit http://localhost:8000


# API Endpoints

| Method | Endpoint     | Description              |
|--------|--------------|--------------------------|
| GET    | `/`          | Welcome message          |
| POST   | `/register`  | Register a new user      |
| POST   | `/login`     | Authenticate and get JWT |
| GET    | `/secure`    | Authenticated user route |



# Author

*Gloria John*  
Penetration Tester | Application Security Engineer | Secure API Development  
