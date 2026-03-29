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
  },
  ariaLabel: {
    type: String,
    default: null
  },
  ariaDescribedBy: {
    type: String,
    default: null
  }
});

// Generate accessible label based on context
const computedAriaLabel = (props) => {
  if (props.ariaLabel) return props.ariaLabel;
  if (props.loading) return 'Loading, please wait';
  return null;
};
</script>

<template>
  <button :type="type" :class="['base-button', `variant-${variant}`]" :disabled="loading || disabled"
    :aria-label="computedAriaLabel" :aria-describedby="ariaDescribedBy" :aria-busy="loading" :aria-disabled="disabled"
    @keydown.enter="!loading && !disabled && $emit('click')"
    @keydown.space.prevent="!loading && !disabled && $emit('click')">
    <span v-if="loading" class="loader" aria-hidden="true"></span>
    <span v-else class="button-content">
      <slot />
    </span>
  </button>
</template>

<style scoped>
.base-button {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  gap: 0.5rem;
  font-family: inherit;

  /* Accessibility: Ensure focus is visible */
  outline: none;
}

/* Focus indicator for keyboard navigation */
.base-button:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
  box-shadow: 0 0 0 2px rgba(0, 138, 0, 0.2);
}

/* Ensure sufficient color contrast */
.variant-primary {
  background-color: var(--primary-color);
  color: white;
}

.variant-primary:hover:not(:disabled) {
  filter: brightness(1.1);
}

.variant-danger {
  background-color: var(--error-color);
  color: white;
}

.variant-danger:hover:not(:disabled) {
  filter: brightness(1.1);
}

.variant-neutral {
  background-color: var(--secondary-color);
  color: white;
}

.variant-neutral:hover:not(:disabled) {
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
  to {
    transform: rotate(360deg);
  }
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .loader {
    animation: none;
  }

  .base-button {
    transition: none;
  }
}
</style>