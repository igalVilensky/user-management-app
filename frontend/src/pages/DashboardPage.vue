<script setup>
import { onMounted, ref } from "vue";
import { useUsers } from "../composables/useUsers";

const { users, fetchUsers, addUser, removeUser } = useUsers();

const showForm = ref(false);
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

async function handleAddUser() {
    if (!newUser.value.first_name || !newUser.value.last_name || !newUser.value.username) {
        alert("First Name, Last Name and Username are required!");
        return;
    }
    await addUser(newUser.value);
    newUser.value = { first_name: "", last_name: "", username: "", phone_number: "", address: "" };
    showForm.value = false;
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
            <input v-model="newUser.first_name" placeholder="First Name" />
            <input v-model="newUser.last_name" placeholder="Last Name" />
            <input v-model="newUser.username" placeholder="Username" />
            <input v-model="newUser.phone_number" placeholder="Phone Number" />
            <input v-model="newUser.address" placeholder="Address" />
            <button @click="handleAddUser">Save</button>
        </div>

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