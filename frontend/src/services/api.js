const API_BASE = "http://127.0.0.1:8000";

async function handleResponse(res) {
    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}

// GET all users
export async function getUsers(skip = 0, limit = 10) {
    const res = await fetch(`${API_BASE}/users/?skip=${skip}&limit=${limit}`);
    return handleResponse(res);
}

// GET single user
export async function getUser(id) {
    const res = await fetch(`${API_BASE}/users/${id}`);
    return handleResponse(res);
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
    return handleResponse(res);
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
    return handleResponse(res);
}

// DELETE user
export async function deleteUser(id) {
    const res = await fetch(`${API_BASE}/users/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}

// Suggest username
export async function suggestUsername(firstName, lastName) {
    const res = await fetch(
        `${API_BASE}/users/suggest-username?first_name=${firstName}&last_name=${lastName}`
    );
    return handleResponse(res);
}