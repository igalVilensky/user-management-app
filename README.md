# 📊 User Administration Application

A full-stack user management dashboard designed for efficient administrative workflows. Built with **FastAPI** and **Vue.js 3**, it provides real-time interactivity, user CRUD operations, and a modular component-based UI.

Repository: [https://github.com/igalVilensky/user-management-app](https://github.com/igalVilensky/user-management-app)

---

## ✨ Key Features

* ⚡ **Real-time CRUD operations** with immediate UI updates and notifications
* 🤖 **Smart username generation** ensuring uniqueness based on user identity
* 🔍 **Global debounced search** across name, username, phone, and address fields
* 📄 **Pagination & sorting** for scalable dataset handling
* 🛡️ **Inline validation & data integrity rules**
* 📱 **Responsive UI** with reusable base components
* 🧩 **Component-based frontend architecture**
* 🐳 **Docker support included (optional setup via docker-compose)**

---

## 🛠️ Technology Stack

### Backend

* **Framework**: FastAPI (Python 3.10+)
* **ORM**: SQLAlchemy 2.0
* **Database**: SQLite (development)
* **Validation**: Pydantic v2
* **Testing**: Pytest

### Frontend

* **Framework**: Vue.js 3 (Composition API)
* **Tooling**: Vite
* **Routing**: Vue Router
* **Styling**: Vanilla CSS with design system approach
* **Architecture**: Reusable base components + composables

---

## 🎨 Design Highlights

* Username generation handled on backend to guarantee consistency and uniqueness
* Clear separation of concerns (routers, services, schemas, models)
* Reusable frontend composables (e.g. `useUsers`, `useAsync`)
* Modular UI system with base components

---

## ♿ Accessibility

* Full keyboard navigation support
* Proper form labeling and validation feedback
* Modal focus management for screen readers
* Semantic search region (`role="search"` usage)
* Live region updates for search results (`aria-live` announcements)
* `aria-controls` linking search input to results table

---

## 🛡️ Error Handling

* Backend validation using Pydantic schemas
* Consistent HTTP error responses (`400`, `404`, `422`)
* Database constraint handling (e.g., uniqueness rules)
* Frontend API layer maps errors into user-friendly messages
* UI-level error propagation for forms and async actions

---

## 🚀 Getting Started

### ⚠️ Prerequisites

Ensure you have:

* Node.js **20+** (required for Vite)
* npm 9+
* Python 3.10+
* python3-venv installed
* Git

---

## Option 1: Docker (Recommended)

> Docker support is included for simplified setup via docker-compose.

```bash
# Clone repository
git clone https://github.com/igalVilensky/user-management-app.git
cd user-management-app

# Start services
docker compose up --build -d
```

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Option 2: Local Development

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```text
.
├── backend/
│   ├── routers/
│   ├── tests/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/styles/
│   │   ├── components/base/
│   │   ├── composables/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── services/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .dockerignore
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🧪 Testing

Backend tests cover CRUD operations and edge cases such as uniqueness constraints.

```bash
cd backend
pytest
```

---

## 📡 API Endpoints

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| GET    | /users/                 | List users (pagination + search) |
| POST   | /users/                 | Create user                      |
| GET    | /users/{id}             | Get user details                 |
| PUT    | /users/{id}             | Update user                      |
| DELETE | /users/{id}             | Delete user                      |
| GET    | /users/suggest-username | Generate username                |

---

## 🛡️ Production Considerations

* Replace SQLite with PostgreSQL for production workloads
* Add authentication & authorization (JWT/OAuth2)
* Add structured logging and monitoring
* Implement rate limiting and health checks

---

## 🧩 Architecture Exploration

An alternative **hexagonal architecture** approach was explored in a separate branch.

Structure:

```text
backend/
├── domain/
├── services/
├── adapters/
└── infrastructure/
```

This improves separation between business logic and infrastructure concerns.

---

## 🛠️ Troubleshooting

* **CORS issues**: ensure backend allows frontend origin (`http://localhost:5173`)
* **Database locks**: avoid concurrent SQLite writes in dev
* **Vite startup issues**: ensure Node.js 20+ is installed
* **Python venv issues**: ensure `python3-venv` is installed
* **Docker networking**: ensure frontend API URL matches backend service
