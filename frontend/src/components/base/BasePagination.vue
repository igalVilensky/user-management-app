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

const totalPages = computed(() =>
  Math.ceil(props.totalItems / props.itemsPerPage)
);

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
  <div class="pagination-wrapper" role="navigation" aria-label="Pagination">
    <!-- Rows per page -->
    <div class="pagination-limit">
      <label for="itemsPerPage" id="rows-label">Rows per page:</label>
      <select id="itemsPerPage" class="pagination-select" :value="itemsPerPage" @change="onItemsPerPageChange"
        aria-labelledby="rows-label">
        <option v-for="option in rowsOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
    </div>

    <!-- Controls -->
    <div v-if="totalPages > 1" class="pagination-controls">
      <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage" aria-label="Previous page"
        :aria-disabled="currentPage === 1">
        ‹
      </button>

      <div class="pagination-info" aria-live="polite" aria-label="Current page">
        {{ currentPage }} / {{ totalPages }}
      </div>

      <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage" aria-label="Next page"
        :aria-disabled="currentPage === totalPages">
        ›
      </button>
    </div>

    <!-- Total -->
    <div class="pagination-total" aria-live="polite">
      {{ totalItems }} total {{ totalItems === 1 ? 'user' : 'users' }}
    </div>
  </div>
</template>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1rem 0;
  border-top: 1px solid var(--border-color);
  margin-top: 1rem;
}

/* Controls */
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Rows per page */
.pagination-limit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* Select */
.pagination-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: white;
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
}

/* Buttons */
.pagination-btn {
  background: white;
  border: 1px solid var(--border-color);
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
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

/* Info */
.pagination-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
  min-width: 60px;
  text-align: center;
}

/* Total */
.pagination-total {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* =========================
   Mobile Optimization
========================= */
@media (max-width: 640px) {
  .pagination-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .pagination-limit,
  .pagination-total {
    justify-content: space-between;
  }

  .pagination-controls {
    justify-content: center;
  }

  .pagination-btn {
    flex: 1;
    padding: 0.6rem;
  }

  .pagination-info {
    min-width: auto;
  }
}
</style>