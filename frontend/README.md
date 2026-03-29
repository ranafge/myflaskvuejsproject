# Flask-VueJS Project

A simple full-stack project using **Flask** as backend and **Vue.js (Vite)** as frontend with **MySQL** database, fully dockerized.

---

## Features

- REST API with Flask
- MySQL database integration
- Data serialization with Marshmallow
- Frontend with Vue.js & Vite
- CORS enabled
- Dockerized setup for easy deployment

---

## Prerequisites

- Docker & Docker Compose
- Basic knowledge of Python and Node.js

---

## Folder Structure


myflaskvuejsproject/
├─ backendDev/ # Flask backend
├─ frontend/ # Vue.js frontend
├─ docker-compose.yml # Docker Compose file
└─ myvenv/ # Optional local Python virtualenv


---

## Setup

1. Clone the project:

```bash
git clone <repo-url>
cd myflaskvuejsproject
Build and run containers:
docker compose up --build -d
Access services:
Backend: http://localhost:5000
Frontend: http://localhost:5173
Environment Variables

Set the following in .env (used by backend):

DB_HOST=db
DB_USER=root
DB_PASSWORD=pass1478
DB_NAME=flask
API Endpoints (Backend)
Method	Endpoint	Description
GET	/get	Get all articles
GET	/get/<id>/	Get article by ID
POST	/add	Add new article
PUT	/update/<id>/	Update article by ID
DELETE	/delete/<id>/	Delete article by ID
Notes
Make sure your Node.js version is 20+ in Dockerfile for frontend.
MySQL client dependencies are installed in backend Dockerfile for mysqlclient.
License

MIT License


এখন আপনি এটাকে সরাসরি **`README.md`** ফাইলে পেস্ট করতে পারেন।  

যদি চাও, আমি চাইলে **এক লাইন কমান্ড দিয়ে সব রান করার আরও ছোট ও সহজ README** বানিয়ে দিতে পারি। সেটা কি বানাই?