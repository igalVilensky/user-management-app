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
  }
});

const emit = defineEmits(['update:currentPage']);

const totalPages = computed(() => Math.ceil(props.totalItems / props.itemsPerPage));

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
  <div v-if="totalPages > 1" class="pagination-wrapper">
    <button 
      class="pagination-btn" 
      :disabled="currentPage === 1" 
      @click="prevPage"
    >
      &lsaquo; Previous
    </button>
    
    <div class="pagination-info">
      Page <strong>{{ currentPage }}</strong> of <strong>{{ totalPages }}</strong>
      <span class="total-items">({{ totalItems }} total)</span>
    </div>
    
    <button 
      class="pagination-btn" 
      :disabled="currentPage === totalPages" 
      @click="nextPage"
    >
      Next &rsaquo;
    </button>
  </div>
</template>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 1.5rem 0;
}

.pagination-btn {
  background: white;
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  color: var(--text-primary);
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
}

.total-items {
  margin-left: 0.5rem;
  font-size: 0.75rem;
}
</style>
