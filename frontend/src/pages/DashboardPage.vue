<script setup>
import { onMounted, ref, watch } from "vue";
import { useUsers } from "../composables/useUsers";
import { suggestUsername } from "../services/api";

const { users, fetchUsers, addUser, removeUser } = useUsers();

const showForm = ref(false);
const error = ref("");

const usernameManuallyEdited = ref(false);
let debounceTimer = null;

const newUser = ref({
    first_name: "",
    last_name: "",
    username: "",
    phone_number: "",
    address: ""
});

onMounted(() => {
    fetchUsers();
});

function editUser(id) {
    console.log("Edit user", id);
}

function handleDelete(id) {
    if (confirm("Are you sure you want to delete this user?")) {
        removeUser(id);
    }
}

// 👇 Track manual username edits
function onUsernameInput() {
    usernameManuallyEdited.value = true;
}

// 👇 Watch first + last name for suggestion
watch(
    () => [newUser.value.first_name, newUser.value.last_name],
    ([first, last]) => {
        if (!first || !last) return;

        // frontend instant suggestion
        if (!usernameManuallyEdited.value) {
            newUser.value.username = `${first}.${last}`.toLowerCase();
        }

        // debounce backend call
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(async () => {
            try {
                const res = await suggestUsername(first, last);

                if (!usernameManuallyEdited.value) {
                    newUser.value.username = res.username;
                }
            } catch (err) {
                console.error(err);
            }
        }, 400);
    }
);

async function handleAddUser() {
    error.value = "";

    if (!newUser.value.first_name || !newUser.value.last_name || !newUser.value.username) {
        error.value = "First Name, Last Name and Username are required";
        return;
    }

    try {
        await addUser(newUser.value);

        newUser.value = {
            first_name: "",
            last_name: "",
            username: "",
            phone_number: "",
            address: ""
        };

        usernameManuallyEdited.value = false;
        showForm.value = false;
    } catch (err) {
        error.value = err.message || "Failed to create user";
    }
}
</script>

<template>
    <div>
        <h1>User Dashboard</h1>

        <!-- Add User Button -->
        <button @click="showForm = !showForm">
            {{ showForm ? "Cancel" : "Add New User" }}
        </button>
        <!-- Add User Form -->
        <div v-if="showForm" style="margin: 10px 0; padding: 10px; border: 1px solid #ccc;">
            <!-- Error message -->
            <p v-if="error" style="color: red;">{{ error }}</p>

            <input v-model="newUser.first_name" placeholder="First Name" />
            <input v-model="newUser.last_name" placeholder="Last Name" />

            <!-- username with manual override detection -->
            <input v-model="newUser.username" @input="onUsernameInput" placeholder="Username" />

            <input v-model="newUser.phone_number" placeholder="Phone Number" />
            <input v-model="newUser.address" placeholder="Address" />

            <button @click="handleAddUser" :disabled="!newUser.first_name || !newUser.last_name || !newUser.username">
                Save
            </button>
        </div>

        <!-- Users Table -->
        <table border="1" cellspacing="0" cellpadding="5">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Username</th>
                    <th>Phone</th>
                    <th>Address</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.first_name }}</td>
                    <td>{{ user.last_name }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.phone_number }}</td>
                    <td>{{ user.address }}</td>
                    <td>
                        <button @click="editUser(user.id)">Edit</button>
                        <button @click="handleDelete(user.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>