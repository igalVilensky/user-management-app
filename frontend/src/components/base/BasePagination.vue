<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalItems: {
    type: Number,
    required: true
  },
  itemsPerPage: {
    type: Number,
    default: 10
  },
  rowsOptions: {
    type: Array,
    default: () => [5, 10, 25, 50]
  }
});

const emit = defineEmits(['update:currentPage', 'update:itemsPerPage']);

const totalPages = computed(() => Math.ceil(props.totalItems / props.itemsPerPage));

function onItemsPerPageChange(event) {
  emit('update:itemsPerPage', Number(event.target.value));
  emit('update:currentPage', 1);
}

function prevPage() {
  if (props.currentPage > 1) {
    emit('update:currentPage', props.currentPage - 1);
  }
}

function nextPage() {
  if (props.currentPage < totalPages.value) {
    emit('update:currentPage', props.currentPage + 1);
  }
}
</script>

<template>
  <div class="pagination-wrapper">
    <div class="pagination-limit">
      <label for="itemsPerPage">Rows per page:</label>
      <select id="itemsPerPage" class="pagination-select" :value="itemsPerPage" @change="onItemsPerPageChange">
        <option v-for="option in rowsOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
    </div>

    <div v-if="totalPages > 1" class="pagination-controls">
      <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage" aria-label="Previous page">
        &lsaquo; Previous
      </button>

      <div class="pagination-info">
        Page <strong>{{ currentPage }}</strong> of <strong>{{ totalPages }}</strong>
      </div>

      <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage" aria-label="Next page">
        Next &rsaquo;
      </button>
    </div>

    <div class="pagination-total">
      <strong>{{ totalItems }}</strong> total users
    </div>
  </div>
</template>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border-color);
  margin-top: 1rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.pagination-limit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.pagination-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: white;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.875rem;
  cursor: pointer;
  transition: border-color 0.2s;
}

.pagination-select:hover {
  border-color: var(--primary-color);
}

.pagination-btn {
  background: white;
  border: 1px solid var(--border-color);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  color: var(--text-primary);
  font-family: inherit;
}

.pagination-btn:hover:not(:disabled) {
  background-color: var(--hover-bg);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
  min-width: 100px;
  text-align: center;
}

.pagination-total {
  font-size: 0.875rem;
  color: var(--text-secondary);
}
</style>