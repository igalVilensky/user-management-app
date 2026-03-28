<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary' // 'primary', 'danger', 'neutral'
  },
  loading: Boolean,
  disabled: Boolean,
  type: {
    type: String,
    default: 'button'
  }
});
</script>

<template>
  <button
    :type="type"
    :class="['base-button', `variant-${variant}`]"
    :disabled="loading || disabled"
  >
    <span v-if="loading" class="loader"></span>
    <slot v-else />
  </button>
</template>

<style scoped>
.base-button {
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  gap: 0.5rem;
}

.variant-primary {
  background-color: var(--primary-color);
  color: white;
}
.variant-primary:hover {
  filter: brightness(1.1);
}

.variant-danger {
  background-color: var(--error-color);
  color: white;
}
.variant-danger:hover {
  filter: brightness(1.1);
}

.variant-neutral {
  background-color: var(--secondary-color);
  color: white;
}
.variant-neutral:hover {
  filter: brightness(1.1);
}

.base-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loader {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
