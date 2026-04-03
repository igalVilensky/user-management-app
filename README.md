# 📊 User Administration Application

A modern, full-stack user management dashboard designed for efficient administrative tasks. Built with FastAPI and Vue.js 3, it offers real-time interactivity, automated username suggestions, and a premium component-based UI.

## ✨ Key Features

*   **⚡ Real-time CRUD**: Manage users with immediate UI feedback and toast notifications.
*   **🤖 Smart Suggestions**: Automatically generates unique usernames based on first and last names.
*   **🔍 Global Search**: Instantly filter users by name, last name, username, phone number, or address with a debounced, accessible search bar.
*   **📄 Seamless Pagination & Sorting**: Handles large datasets with a robust pagination system and dynamic column sorting.
*   **🛡️ Data Integrity**: Inline validation for fields and phone number masks.
*   **📱 Responsive & Premium UI**: A clean, modern interface that works across all devices.
*   **🐳 Containerized**: Fully Dockerized for "one-click" development and deployment.

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) 2.0
- **Database**: [SQLite](https://www.sqlite.org/) (File-based)
- **Validation**: [Pydantic](https://docs.pydantic.dev/) v2
- **Testing**: [Pytest](https://docs.pytest.org/)

### Frontend
- **Framework**: [Vue.js 3](https://vuejs.org/) (Composition API)
- **Tooling**: [Vite](https://vitejs.dev/)
- **Routing**: [Vue Router](https://router.vuejs.org/)
- **Styling**: Vanilla CSS with a modern design system.
- **Components**: Reusable base component library (`BaseButton`, `BaseTable`, etc.)

---

## 🎨 Design Highlights

- **Username suggestion handled on the backend** to ensure uniqueness and consistency.
- **Clean separation of concerns** between routers, schemas, and models for maintainability.
- **Reusable frontend logic** via Vue composables (e.g., `useUsers`, `useAsync`).
- **Dockerized setup** ensuring consistent and reproducible environments across development and deployment.

---

## ♿ Accessibility

- **Full keyboard navigation support** (tab-based interaction).
- **Accessible form inputs** with proper labeling and validation feedback.
- **Modal focus management** to ensure correct accessibility for assistive technologies.
- **Search landmark** (`<search>` element with `role="search"`) for quick navigation by screen reader users.
- **Live result announcements**: a `aria-live` region announces the result count after each search (e.g. *"5 users found."*).
- **`aria-controls`** links the search input to the data table for full semantic association.

---

## 🛡️ Error Handling

- **Robust error handling across backend and frontend**:
  - Backend enforces strict validation and handles database integrity errors gracefully (e.g., unique constraints).
  - API explicitly returns consistent HTTP error responses (e.g., `400 Bad Request`, `422 Unprocessable Entity`, `404 Not Found`).
  - Frontend (`api.js`) maps HTTP errors and 422 validations into user-friendly messages.
  - Frontend UI propagates and transparently displays errors in real-time within forms and across async operations.

---

## 🚀 Getting Started

### Option 1: Docker (Recommended)
The easiest way to start the entire stack is using Docker Compose.

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd user-management-app
    ```
2.  **Start the services**:
    ```bash
    docker-compose up --build -d
    ```
    - Frontend: [http://localhost:5173](http://localhost:5173)
    - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2: Local Development

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### 2. Frontend Setup
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
│   │   ├── __init__.py
│   │   └── user_routes.py     # API endpoint definitions
│   ├── tests/
│   │   ├── conftest.py        # Test configuration
│   │   ├── test_main.py       # Root API tests
│   │   └── test_users.py      # CRUD operation tests
│   ├── database.py            # SQLite engine & session config
│   ├── main.py                # FastAPI application entry
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic validation schemas
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container config
│   └── .dockerignore
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/styles/     # Global CSS and themes
│   │   ├── components/base/   # Atomic UI components
│   │   ├── composables/       # Reusable logic (useUsers, useAsync)
│   │   ├── pages/             # Main application views
│   │   ├── router/            # Vue Router configuration
│   │   ├── services/          # API communication (api.js)
│   │   ├── App.vue            # Root component
│   │   └── main.js            # Frontend entry point
│   ├── package.json           # Dependencies and scripts
│   ├── vite.config.js         # Build and dev server config
│   ├── Dockerfile             # Frontend container config
│   └── .dockerignore
├── .gitignore
├── README.md
└── docker-compose.yml         # Container orchestration
```

## 🧪 Testing

The backend includes a comprehensive test suite covering all CRUD operations and specific edge cases like duplicate usernames.

```bash
cd backend
# With venv active
pytest
```

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/users/` | Fetch paginated, sorted, and optionally filtered list of users (`?search=`) |
| **POST** | `/users/` | Register a new user |
| **GET** | `/users/{id}` | Retrieve specific user details |
| **PUT** | `/users/{id}` | Update existing user information |
| **DELETE** | `/users/{id}` | Remove a user record |
| **GET** | `/users/suggest-username` | Get an algorithmic username suggestion |

---

## 🛡️ Production Considerations

- **Database**: Replace SQLite with PostgreSQL for higher concurrency and ACID compliance in production.
- **Security**: Add a robust authentication and authorization layer (e.g., JWT, OAuth2).
- **Observability**: Implement structured logging, rate limiting, and health checks.

---

## 🧩 Alternative Architecture (Hexagonal)

In addition to the main implementation, I explored a second approach using a **hexagonal (ports & adapters)** architecture in a separate branch.

This version explicitly separates:
- **Domain layer** (business entities and logic)
- **Application layer** (services and use cases)
- **Ports & Adapters** (interfaces and infrastructure implementations)

Example structure from that approach:

```text
backend/
├── domain/
│   ├── entities/
│   └── ports/
├── services/
├── adapters/
│   ├── db/
│   └── web/
└── infrastructure/
```

---

## 🛠️ Troubleshooting

- **CORS Errors**: Ensure the backend `main.py` has the correct `allow_origins`. Default development origin is `http://localhost:5173`.
- **Database Locked**: If multiple processes try to write to the SQLite database, you may see a "database locked" error. Use only one instance of the app or wait for operations to finish.
- **Docker Networking**: In Docker, the frontend communicates with the backend via the container name or exposed port. Ensure `frontend/src/services/api.js` points to the correct backend address.

