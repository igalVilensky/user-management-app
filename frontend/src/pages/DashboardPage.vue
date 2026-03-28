<script setup>
import { onMounted, ref, watch } from "vue";
import { useUsers } from "../composables/useUsers";
import { suggestUsername } from "../services/api";

// Base Components
import BaseButton from "../components/base/BaseButton.vue";
import BaseInput from "../components/base/BaseInput.vue";
import BaseModal from "../components/base/BaseModal.vue";
import BaseTable from "../components/base/BaseTable.vue";
import BasePagination from "../components/base/BasePagination.vue";
import BaseCard from "../components/base/BaseCard.vue";
import BaseToast from "../components/base/BaseToast.vue";
import { computed } from "vue";

const {
  users,
  totalUsers,
  page,
  limit,
  loading,
  error,
  fetchUsers,
  addUser,
  editUser,
  removeUser
} = useUsers();

const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const userToDelete = ref(null);
const editingUser = ref(null);
const successMessage = ref("");
const createError = ref("");
const editError = ref("");
const usernameManuallyEdited = ref(false);
const isCreating = ref(false);
const isEditing = ref(false);
const isDeleting = ref(false);
let debounceTimer = null;

// Validation States
const newUserErrors = ref({
  first_name: "",
  last_name: "",
  username: "",
  phone_number: ""
});

const editingUserErrors = ref({
  first_name: "",
  last_name: "",
  username: "",
  phone_number: ""
});

function validateField(field, value) {
  if (!value && ['first_name', 'last_name', 'username'].includes(field)) {
    return "This field is required";
  }

  if (['first_name', 'last_name'].includes(field)) {
    if (value && !/^[a-zA-Z\s\-']{1,50}$/.test(value)) {
      return "Only letters, spaces, hyphens, or apostrophes allowed (up to 50 chars)";
    }
  }

  if (field === 'username') {
    if (value && value.length < 3) {
      return "Username must be at least 3 characters";
    }
    if (value && value.length > 50) {
      return "Username must be 50 characters or less";
    }
  }

  if (field === 'phone_number') {
    if (value && !/^[\+\d\s\-\(\)]{8,20}$/.test(value)) {
      return "Invalid format (8-20 chars: numbers, spaces, -, (, ), +)";
    }
  }

  return "";
}

const hasCreateErrors = computed(() => {
  return Object.values(newUserErrors.value).some(error => error !== "") ||
    !newUser.value.first_name || !newUser.value.last_name || !newUser.value.username;
});

const hasEditErrors = computed(() => {
  return Object.values(editingUserErrors.value).some(error => error !== "") ||
    (editingUser.value && (!editingUser.value.first_name || !editingUser.value.last_name || !editingUser.value.username));
});

const initialNewUser = {
  first_name: "",
  last_name: "",
  username: "",
  phone_number: "",
  address: ""
};

const newUser = ref({ ...initialNewUser });

onMounted(() => {
  fetchUsers();
});

// Watch page and limit for pagination changes
watch([page, limit], () => {
  fetchUsers();
});

// Watch first + last name for username suggest
watch(
  () => [newUser.value.first_name, newUser.value.last_name],
  ([first, last]) => {
    // Validate names immediately
    newUserErrors.value.first_name = validateField('first_name', first);
    newUserErrors.value.last_name = validateField('last_name', last);

    if (!first || !last) return;

    // Clear existing timer
    if (debounceTimer) clearTimeout(debounceTimer);

    // Set initial suggestion
    if (!usernameManuallyEdited.value) {
      newUser.value.username = `${first}.${last}`.toLowerCase().replace(/\s/g, '');
    }

    // Debounce API call to avoid too many requests
    debounceTimer = setTimeout(async () => {
      try {
        const res = await suggestUsername(first, last);
        if (!usernameManuallyEdited.value) {
          newUser.value.username = res.username;
        }
      } catch (err) {
        console.error("Suggest error:", err);
      }
    }, 500);
  }
);

// Watch username and phone for validation
watch(() => newUser.value.username, (val) => {
  newUserErrors.value.username = validateField('username', val);
});

watch(() => newUser.value.phone_number, (val) => {
  newUserErrors.value.phone_number = validateField('phone_number', val);
});

// Watch editing user for validation
watch(() => editingUser.value, (val) => {
  if (!val) return;
  editingUserErrors.value.first_name = validateField('first_name', val.first_name);
  editingUserErrors.value.last_name = validateField('last_name', val.last_name);
  editingUserErrors.value.username = validateField('username', val.username);
  editingUserErrors.value.phone_number = validateField('phone_number', val.phone_number);
}, { deep: true });

function showToast(msg) {
  successMessage.value = msg;
}

function onUsernameInput() {
  usernameManuallyEdited.value = true;
}

function resetForm() {
  newUser.value = { ...initialNewUser };
  newUserErrors.value = {
    first_name: "",
    last_name: "",
    username: "",
    phone_number: ""
  };
  usernameManuallyEdited.value = false;
  createError.value = "";
}

async function handleAddUser() {
  createError.value = "";
  isCreating.value = true;
  try {
    await addUser(newUser.value);
    showCreateModal.value = false;
    resetForm();
    showToast("User created successfully!");
  } catch (err) {
    createError.value = err.message || "Failed to create user";
  } finally {
    isCreating.value = false;
  }
}

function openEditModal(user) {
  editingUser.value = { ...user };
  editingUserErrors.value = {
    first_name: "",
    last_name: "",
    username: "",
    phone_number: ""
  };
  usernameManuallyEdited.value = false;
  editError.value = "";
  showEditModal.value = true;
}

function onEditUsernameInput() {
  usernameManuallyEdited.value = true;
}

async function handleUpdateUser() {
  if (!editingUser.value) return;
  editError.value = "";
  isEditing.value = true;
  try {
    await editUser(editingUser.value.id, editingUser.value);
    showEditModal.value = false;
    showToast("User updated successfully!");
  } catch (err) {
    editError.value = err.message || "Failed to update user";
  } finally {
    isEditing.value = false;
  }
}

function confirmDelete(user) {
  userToDelete.value = user;
  showDeleteModal.value = true;
}

async function handleDelete() {
  if (!userToDelete.value) return;
  isDeleting.value = true;
  try {
    await removeUser(userToDelete.value.id);
    showDeleteModal.value = false;
    userToDelete.value = null;
    showToast("User deleted successfully!");
  } catch (err) {
    alert("Failed to delete user: " + err.message);
  } finally {
    isDeleting.value = false;
  }
}

const tableColumns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'first_name', label: 'First Name', width: '130px' },
  { key: 'last_name', label: 'Last Name', width: '130px' },
  { key: 'username', label: 'Username', width: '130px' },
  { key: 'phone_number', label: 'Phone', width: '120px' },
  { key: 'address', label: 'Address', width: 'auto' },
  { key: 'actions', label: 'Actions', width: '170px' }
];
</script>

<template>
  <div class="container">
    <header class="dashboard-header">
      <h1>User Administration</h1>
      <BaseButton variant="primary" @click="showCreateModal = true">
        + Add User
      </BaseButton>
    </header>

    <BaseCard>
      <div v-if="error" class="cta-container error-state">
        <p style="color: var(--error-color)">{{ error }}</p>
        <BaseButton variant="neutral" @click="fetchUsers">Try Again</BaseButton>
      </div>

      <template v-else>
        <BaseTable :columns="tableColumns" :data="users" :loading="loading" empty-text="No users found in the system.">
          <template #cell(actions)="{ row }">
            <div class="actions-cell">
              <BaseButton variant="neutral" @click="openEditModal(row)">
                <span class="icon">✏️</span> Edit
              </BaseButton>
              <BaseButton variant="danger" @click="confirmDelete(row)">
                <span class="icon">🗑</span> Delete
              </BaseButton>
            </div>
          </template>

          <template #empty-cta>
            <BaseButton variant="primary" @click="showCreateModal = true">
              Create First User
            </BaseButton>
          </template>
        </BaseTable>

        <BasePagination v-model:currentPage="page" v-model:itemsPerPage="limit" :totalItems="totalUsers" />
      </template>
    </BaseCard>

    <!-- Create User Modal -->
    <BaseModal :show="showCreateModal" title="Create New User" @close="showCreateModal = false">
      <template #default>
        <div v-if="createError" class="error-message">
          {{ createError }}
        </div>
        <div class="modal-form">
          <BaseInput v-model="newUser.first_name" label="First Name" placeholder="Enter first name"
            :error="newUserErrors.first_name" required />
          <BaseInput v-model="newUser.last_name" label="Last Name" placeholder="Enter last name"
            :error="newUserErrors.last_name" required />
          <BaseInput v-model="newUser.username" label="Username" placeholder="Confirm or change username"
            :error="newUserErrors.username" @input="onUsernameInput" required />
          <BaseInput v-model="newUser.phone_number" label="Telephone Number" placeholder="e.g. +49 123 456789"
            :error="newUserErrors.phone_number" />
          <BaseInput v-model="newUser.address" label="Address" placeholder="Street, City, ZIP" />
        </div>
      </template>

      <template #footer>
        <BaseButton variant="neutral" @click="resetForm">
          Reset
        </BaseButton>
        <BaseButton variant="primary" :loading="isCreating" :disabled="hasCreateErrors" @click="handleAddUser">
          Create User
        </BaseButton>
      </template>
    </BaseModal>

    <!-- Edit User Modal -->
    <BaseModal :show="showEditModal" title="Edit User" @close="showEditModal = false">
      <template #default>
        <div v-if="editError" class="error-message">
          {{ editError }}
        </div>

        <div v-if="editingUser" class="modal-form">
          <BaseInput v-model="editingUser.first_name" label="First Name" :error="editingUserErrors.first_name" />
          <BaseInput v-model="editingUser.last_name" label="Last Name" :error="editingUserErrors.last_name" />
          <BaseInput v-model="editingUser.username" label="Username" :error="editingUserErrors.username"
            @input="onEditUsernameInput" />
          <BaseInput v-model="editingUser.phone_number" label="Telephone Number" :error="editingUserErrors.phone_number" />
          <BaseInput v-model="editingUser.address" label="Address" />
        </div>
      </template>

      <template #footer>
        <BaseButton variant="neutral" @click="showEditModal = false">
          Cancel
        </BaseButton>
        <BaseButton variant="primary" :loading="isEditing" :disabled="hasEditErrors" @click="handleUpdateUser">
          Save Changes
        </BaseButton>
      </template>
    </BaseModal>

    <!-- Delete Confirmation Modal -->
    <BaseModal :show="showDeleteModal" title="Confirm Deletion" @close="showDeleteModal = false">
      <p v-if="userToDelete">
        Are you sure you want to delete user <strong>{{ userToDelete.first_name }} {{ userToDelete.last_name
        }}</strong>?
        <br>This action cannot be undone.
      </p>
      <template #footer>
        <BaseButton variant="neutral" @click="showDeleteModal = false">Cancel</BaseButton>
        <BaseButton variant="danger" :loading="isDeleting" @click="handleDelete">
          Delete Forever
        </BaseButton>
      </template>
    </BaseModal>

    <!-- Toasts -->
    <BaseToast v-if="successMessage" :message="successMessage" @close="successMessage = ''" />
  </div>
</template>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  margin: 0;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error-state {
  border-color: var(--error-color);
  background: rgba(215, 0, 0, 0.05);
}

.error-message {
  color: var(--error-color, #d70000);
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(215, 0, 0, 0.05);
  border-radius: 6px;
  font-size: 0.875rem;
  border-left: 3px solid var(--error-color, #d70000);
}
</style>