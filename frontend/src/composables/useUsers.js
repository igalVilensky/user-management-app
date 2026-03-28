import { ref } from "vue";
import {
    getUsers,
    createUser,
    updateUser,
    deleteUser,
} from "../services/api";

export function useUsers() {
    const users = ref([]);
    const totalUsers = ref(0);
    const page = ref(1);
    const limit = ref(10);
    const loading = ref(false);
    const error = ref(null);

    async function fetchUsers() {
        loading.value = true;
        error.value = null;
        try {
            const skip = (page.value - 1) * limit.value;
            const res = await getUsers(skip, limit.value);
            users.value = res.users;
            totalUsers.value = res.total_count;
        } catch (err) {
            error.value = err.message || "Failed to fetch users";
            console.error(err);
        } finally {
            loading.value = false;
        }
    }

    async function addUser(user) {
        await createUser(user);
        await fetchUsers(); // Re-fetch to update count and list
    }

    async function editUser(id, user) {
        await updateUser(id, user);
        // We can update locally or re-fetch. 
        // For inline editing, local update is smoother, but re-fetch is safer.
        await fetchUsers();
    }

    async function removeUser(id) {
        await deleteUser(id);
        // If we are on a page that becomes empty, go back
        if (users.value.length === 1 && page.value > 1) {
            page.value--;
        }
        await fetchUsers();
    }

    return {
        users,
        totalUsers,
        page,
        limit,
        loading,
        error,
        fetchUsers,
        addUser,
        editUser,
        removeUser,
    };
}