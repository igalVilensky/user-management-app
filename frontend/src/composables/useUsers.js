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
    const sortBy = ref(null);
    const sortOrder = ref('asc');
    const loading = ref(false);
    const error = ref(null);
    const creating = ref(false);
    const updating = ref(false);
    const deleting = ref(false);

    async function fetchUsers() {
        loading.value = true;
        error.value = null;
        try {
            const skip = (page.value - 1) * limit.value;
            const res = await getUsers(skip, limit.value, sortBy.value, sortOrder.value);
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
        creating.value = true;
        try {
            await createUser(user);
            // If we're not on page 1, go to page 1 to see new user
            if (page.value !== 1) {
                page.value = 1;
            } else {
                await fetchUsers();
            }
        } catch (err) {
            throw err;
        } finally {
            creating.value = false;
        }
    }

    async function editUser(id, user) {
        updating.value = true;
        try {
            await updateUser(id, user);
            await fetchUsers();
        } catch (err) {
            throw err;
        } finally {
            updating.value = false;
        }
    }

    async function removeUser(id) {
        deleting.value = true;
        try {
            await deleteUser(id);
            // If we're on last item and not first page, go back
            if (users.value.length === 1 && page.value > 1) {
                page.value--;
            }
            await fetchUsers();
        } catch (err) {
            throw err;
        } finally {
            deleting.value = false;
        }
    }

    return {
        users,
        totalUsers,
        page,
        limit,
        sortBy,
        sortOrder,
        loading,
        error,
        creating,
        updating,
        deleting,
        fetchUsers,
        addUser,
        editUser,
        removeUser,
    };
}