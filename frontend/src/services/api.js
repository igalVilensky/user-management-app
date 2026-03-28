const API_BASE = "http://127.0.0.1:8000";

// GET all users
export async function getUsers() {
    const res = await fetch(`${API_BASE}/users/`);
    return res.json();
}

// GET single user
export async function getUser(id) {
    const res = await fetch(`${API_BASE}/users/${id}`);
    return res.json();
}

// CREATE user
export async function createUser(data) {
    const res = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return res.json();
}

// UPDATE user
export async function updateUser(id, data) {
    const res = await fetch(`${API_BASE}/users/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return res.json();
}

// DELETE user
export async function deleteUser(id) {
    const res = await fetch(`${API_BASE}/users/${id}`, {
        method: "DELETE",
    });
    return res.json();
}