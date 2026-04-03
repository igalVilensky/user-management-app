<script setup>
import { onMounted, ref, watch, computed } from "vue";
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

const {
  users,
  totalUsers,
  page,
  limit,
  sortBy,
  sortOrder,
  searchQuery,
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
const originalEditingUser = ref(null);
const successMessage = ref("");
const createError = ref("");
const editError = ref("");
const usernameManuallyEdited = ref(false);
const isCreating = ref(false);
const isEditing = ref(false);
const isDeleting = ref(false);
let debounceTimer = null;

// Accessibility: Focus management for modals
const createModalRef = ref(null);
const editModalRef = ref(null);
const deleteModalRef = ref(null);

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

const hasChanges = computed(() => {
  if (!editingUser.value || !originalEditingUser.value) return false;

  return JSON.stringify(editingUser.value) !== JSON.stringify(originalEditingUser.value);
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

// Watch pagination and sorting changes
watch([page, limit, sortBy, sortOrder], () => {
  fetchUsers();
});

// Debounced search: reset to page 1 and refetch
let searchDebounceTimer = null;
watch(searchQuery, () => {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    page.value = 1;
    fetchUsers();
  }, 300);
});

// Screen reader announcement for search results
const searchResultsAnnouncement = computed(() => {
  if (loading.value) return '';
  if (!searchQuery.value) return '';
  const count = totalUsers.value;
  return count === 0
    ? 'No users found for your search.'
    : `${count} user${count === 1 ? '' : 's'} found.`;
});

function handleSort(key) {
  if (sortBy.value === key) {
    if (sortOrder.value === 'asc') {
      sortOrder.value = 'desc';
    } else {
      sortBy.value = null;
      sortOrder.value = 'asc';
    }
  } else {
    sortBy.value = key;
    sortOrder.value = 'asc';
  }
  page.value = 1;
}

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

// Watch editing user for validation and changes
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
    // Announce error to screen readers
    const errorElement = document.querySelector('[role="alert"]');
    if (errorElement) {
      errorElement.focus();
    }
  } finally {
    isCreating.value = false;
  }
}

function openEditModal(user) {
  originalEditingUser.value = JSON.parse(JSON.stringify(user));
  editingUser.value = JSON.parse(JSON.stringify(user));
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

  if (!hasChanges.value) {
    showEditModal.value = false;
    return;
  }

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
  { key: 'first_name', label: 'First Name', width: '130px', sortable: true },
  { key: 'last_name', label: 'Last Name', width: '130px', sortable: true },
  { key: 'username', label: 'Username', width: '130px' },
  { key: 'phone_number', label: 'Phone', width: '120px' },
  { key: 'address', label: 'Address', width: 'auto' },
  { key: 'actions', label: 'Actions', width: '170px' }
];
</script>

<template>
  <div class="container">
    <header class="dashboard-header">
      <h1 tabindex="-1">User Administration</h1>
      <BaseButton variant="primary" @click="showCreateModal = true" aria-label="Add new user">
        + Add User
      </BaseButton>
    </header>

    <!-- Search bar -->
    <search class="search-bar" role="search" aria-label="Search users">
      <label for="user-search" class="sr-only">Search users by name, username, phone or address</label>
      <div class="search-input-wrapper">
        <span class="search-icon" aria-hidden="true">🔍</span>
        <input
          id="user-search"
          v-model="searchQuery"
          type="search"
          placeholder="Search by name, username, phone or address…"
          class="search-input"
          autocomplete="off"
          aria-controls="users-table"
          :aria-busy="loading"
        />
        <button
          v-if="searchQuery"
          type="button"
          class="search-clear"
          @click="searchQuery = ''"
          aria-label="Clear search"
        >✕</button>
      </div>
    </search>

    <!-- Live region for CRUD and search result announcements -->
    <div class="sr-only" aria-live="polite" role="status">
      {{ successMessage || searchResultsAnnouncement }}
    </div>

    <BaseCard>
      <!-- Live region for error announcements -->
      <div v-if="error" class="cta-container error-state" role="alert" aria-live="assertive">
        <p style="color: var(--error-color)">{{ error }}</p>
        <BaseButton variant="neutral" @click="fetchUsers">Try Again</BaseButton>
      </div>

      <template v-else>
        <BaseTable id="users-table" :columns="tableColumns" :data="users" :loading="loading" empty-text="No users found in the system."
          aria-label="Users table" :sort-by="sortBy" :sort-order="sortOrder" @sort="handleSort">
          <template #cell(actions)="{ row }">
            <div class="actions-cell">
              <BaseButton variant="neutral" @click="openEditModal(row)"
                :aria-label="`Edit user ${row.first_name} ${row.last_name}`">
                <span class="icon" aria-hidden="true">✏️</span>
                Edit
              </BaseButton>
              <BaseButton variant="danger" @click="confirmDelete(row)"
                :aria-label="`Delete user ${row.first_name} ${row.last_name}`">
                <span class="icon" aria-hidden="true">🗑</span>
                Delete
              </BaseButton>
            </div>
          </template>

          <template #empty-cta>
            <BaseButton variant="primary" @click="showCreateModal = true">
              Create First User
            </BaseButton>
          </template>
        </BaseTable>

        <BasePagination v-model:currentPage="page" v-model:itemsPerPage="limit" :totalItems="totalUsers"
          aria-label="User list pagination" />
      </template>
    </BaseCard>

    <!-- ========== CREATE USER MODAL ========== -->
    <BaseModal ref="createModalRef" :show="showCreateModal" title="Create New User" @close="showCreateModal = false">
      <template #default>
        <div v-if="createError" class="error-message" role="alert" aria-live="assertive">
          {{ createError }}
        </div>
        <div class="modal-form">
          <BaseInput v-model="newUser.first_name" label="First Name" placeholder="Enter first name"
            :error="newUserErrors.first_name" required autocomplete="given-name" />
          <BaseInput v-model="newUser.last_name" label="Last Name" placeholder="Enter last name"
            :error="newUserErrors.last_name" required autocomplete="family-name" />
          <BaseInput v-model="newUser.username" label="Username" placeholder="Confirm or change username"
            :error="newUserErrors.username" @input="onUsernameInput" required />
          <BaseInput v-model="newUser.phone_number" label="Telephone Number" placeholder="e.g. +49 123 456789"
            :error="newUserErrors.phone_number" autocomplete="tel" />
          <BaseInput v-model="newUser.address" label="Address" placeholder="Street, City, ZIP"
            autocomplete="street-address" />
        </div>
      </template>

      <template #footer>
        <BaseButton variant="neutral" @click="resetForm">Reset</BaseButton>
        <BaseButton variant="primary" :loading="isCreating" :disabled="hasCreateErrors" @click="handleAddUser"
          aria-label="Create new user">
          Create User
        </BaseButton>
      </template>
    </BaseModal>



    <!-- ========== EDIT USER MODAL ========== -->
    <BaseModal ref="editModalRef" :show="showEditModal" title="Edit User" @close="showEditModal = false">
      <template #default>
        <div v-if="editError" class="error-message" role="alert" aria-live="assertive">
          {{ editError }}
        </div>
        <div v-if="editingUser" class="modal-form">
          <BaseInput v-model="editingUser.first_name" label="First Name" :error="editingUserErrors.first_name" required
            autocomplete="given-name" />
          <BaseInput v-model="editingUser.last_name" label="Last Name" :error="editingUserErrors.last_name" required
            autocomplete="family-name" />
          <BaseInput v-model="editingUser.username" label="Username" :error="editingUserErrors.username"
            @input="onEditUsernameInput" required autocomplete="username" />
          <BaseInput v-model="editingUser.phone_number" label="Telephone Number" :error="editingUserErrors.phone_number"
            autocomplete="tel" />
          <BaseInput v-model="editingUser.address" label="Address" autocomplete="street-address" />
        </div>
      </template>

      <template #footer>
        <BaseButton variant="neutral" @click="showEditModal = false">Cancel</BaseButton>
        <BaseButton variant="primary" :loading="isEditing" :disabled="hasEditErrors || !hasChanges"
          @click="handleUpdateUser" aria-label="Save user changes">
          Save Changes
        </BaseButton>
      </template>
    </BaseModal>

    <!-- ========== DELETE CONFIRMATION MODAL ========== -->
    <BaseModal ref="deleteModalRef" :show="showDeleteModal" title="Confirm Deletion" @close="showDeleteModal = false">
      <p v-if="userToDelete" id="delete-confirmation-message">
        Are you sure you want to delete user <strong>{{ userToDelete.first_name }} {{ userToDelete.last_name
        }}</strong>?
        <br>This action cannot be undone.
      </p>
      <template #footer>
        <BaseButton variant="neutral" @click="showDeleteModal = false">Cancel</BaseButton>
        <BaseButton variant="danger" :loading="isDeleting" @click="handleDelete"
          aria-label="Confirm permanent deletion">
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

.search-bar {
  margin-bottom: 1.5rem;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 480px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  font-size: 0.9rem;
  pointer-events: none;
  opacity: 0.5;
}

.search-input {
  width: 100%;
  padding: 0.6rem 2.25rem 0.6rem 2.25rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: inherit;
  background: white;
  color: var(--text-primary);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--focus-ring-color);
}

/* Hide browser default clear button for search inputs */
.search-input::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}

.search-clear {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 0.85rem;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease, background 0.15s ease;
}

.search-clear:hover {
  color: var(--text-primary);
  background: var(--hover-bg);
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

.base-button .button-content {
  display: inline-flex;
  align-items: center;
}

.base-button .button-content .icon {
  display: inline-flex;
  align-items: center;
  margin-right: 0.2rem;
}
</style>