import { ref } from "vue";
import {
    getUsers,
    createUser,
    updateUser,
    deleteUser,
} from "../services/api";

export function useUsers() {
    const users = ref([]);
    const loading = ref(false);

    async function fetchUsers() {
        loading.value = true;
        users.value = await getUsers();
        loading.value = false;
    }

    async function addUser(user) {
        await createUser(user);
        await fetchUsers();
    }

    async function editUser(id, user) {
        await updateUser(id, user);
        await fetchUsers();
    }

    async function removeUser(id) {
        await deleteUser(id);
        await fetchUsers();
    }

    return {
        users,
        loading,
        fetchUsers,
        addUser,
        editUser,
        removeUser,
    };
}