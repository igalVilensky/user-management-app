# User Administration Application

A simple web application for managing users in a database with CRUD operations and automatic username suggestion.

## Features

* Create, Read, Update, Delete users
* Automatic username suggestion based on first and last name
* Pagination for user list
* Responsive design (desktop and mobile)
* Input validation (names, phone numbers)
* Toast notifications for user actions

## Tech Stack

* **Backend**: Python with FastAPI, SQLite, SQLAlchemy
* **Frontend**: Vue.js 3 with Composition API
* **Database**: SQLite

## Prerequisites

* Python 3.8 or higher
* Node.js 16 or higher
* npm or yarn

## Installation

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### 1. Start the Backend Server

```bash
cd backend
python main.py
```

The backend will run at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will run at [http://localhost:5173](http://localhost:5173)

### 3. Access the Application

Open your browser and navigate to [http://localhost:5173](http://localhost:5173)

## API Endpoints

| Method | Endpoint                | Description                           |
| ------ | ----------------------- | ------------------------------------- |
| GET    | /users/                 | Get paginated user list               |
| GET    | /users/{id}             | Get single user                       |
| POST   | /users/                 | Create new user                       |
| PUT    | /users/{id}             | Update user                           |
| DELETE | /users/{id}             | Delete user                           |
| GET    | /users/suggest-username | Suggest username from first/last name |

## Project Structure

```
├── backend/
│   ├── routers/
│   │   └── user_routes.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── base/
│   │   │       ├── BaseButton.vue
│   │   │       ├── BaseCard.vue
│   │   │       ├── BaseInput.vue
│   │   │       ├── BaseModal.vue
│   │   │       ├── BasePagination.vue
│   │   │       ├── BaseSkeleton.vue
│   │   │       ├── BaseTable.vue
│   │   │       └── BaseToast.vue
│   │   ├── composables/
│   │   │   ├── useAsync.js
│   │   │   └── useUsers.js
│   │   ├── pages/
│   │   │   ├── DashboardPage.vue
│   │   │   └── NotFoundPage.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Usage

### Creating a User

1. Click the "Add User" button
2. Enter first name and last name
3. Username is automatically suggested (you can modify it)
4. Fill in optional fields (phone number, address)
5. Click "Create User"

### Editing a User

1. Click the "Edit" button next to a user
2. Modify any fields
3. Click "Save Changes"

### Deleting a User

1. Click the "Delete" button next to a user
2. Confirm deletion in the modal

## Troubleshooting

### Backend won't start

* Ensure port 8000 is not in use
* Check if SQLite has write permissions in the backend folder
* Run `pip install -r requirements.txt` again

### Frontend won't start

* Ensure port 5173 is not in use
* Run `npm install` again
* Delete `node_modules` and run `npm install` fresh

### CORS errors

* Ensure backend is running on [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Check that CORS middleware in main.py allows frontend origin

## License

This project was created for assessment purposes.
