const API_BASE = "http://127.0.0.1:8000";

async function handleResponse(res) {
    const contentType = res.headers.get("content-type");
    const hasBody = contentType && contentType.includes("application/json");

    let data = null;
    if (hasBody) {
        try {
            data = await res.json();
        } catch (e) {
            if (!res.ok) {
                throw new Error("Invalid response from server");
            }
        }
    }

    if (!res.ok) {
        // Handle FastAPI validation errors (422)
        if (res.status === 422 && data?.detail) {
            const validationErrors = data.detail.map(err => {
                const field = err.loc[err.loc.length - 1];
                return `${field}: ${err.msg}`;
            }).join(", ");
            throw new Error(validationErrors);
        }

        // Handle custom API errors
        const errorMessage = data?.detail || data?.message || `HTTP ${res.status}: ${res.statusText}`;
        throw new Error(errorMessage);
    }

    return data;
}

// GET all users with pagination
export async function getUsers(skip = 0, limit = 10, sortBy = null, sortOrder = 'asc', search = null) {
    let url = `${API_BASE}/users?skip=${skip}&limit=${limit}`;
    if (sortBy) {
        url += `&sort_by=${encodeURIComponent(sortBy)}&sort_order=${encodeURIComponent(sortOrder)}`;
    }
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }
    const res = await fetch(url);
    return handleResponse(res);
}

// GET single user
export async function getUser(id) {
    if (!id) throw new Error("User ID is required");
    const res = await fetch(`${API_BASE}/users/${id}`);
    return handleResponse(res);
}

// CREATE user
export async function createUser(userData) {
    if (!userData.first_name || !userData.last_name || !userData.username) {
        throw new Error("First name, last name, and username are required");
    }

    const res = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    });
    return handleResponse(res);
}

// UPDATE user
export async function updateUser(id, userData) {
    if (!id) throw new Error("User ID is required");

    const res = await fetch(`${API_BASE}/users/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    });
    return handleResponse(res);
}

// DELETE user
export async function deleteUser(id) {
    if (!id) throw new Error("User ID is required");

    const res = await fetch(`${API_BASE}/users/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}

// Suggest username
export async function suggestUsername(firstName, lastName) {
    if (!firstName || !lastName) {
        throw new Error("First name and last name are required");
    }

    const res = await fetch(
        `${API_BASE}/users/suggest-username?first_name=${encodeURIComponent(firstName)}&last_name=${encodeURIComponent(lastName)}`
    );
    return handleResponse(res);
}