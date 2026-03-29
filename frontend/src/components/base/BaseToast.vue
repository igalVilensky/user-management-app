<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'success'
  },
  duration: {
    type: Number,
    default: 3000
  }
});

const emit = defineEmits(['close']);
const visible = ref(true);

let timeoutId = null;

onMounted(() => {
  if (props.duration > 0) {
    timeoutId = setTimeout(() => {
      visible.value = false;
      setTimeout(() => emit('close'), 300);
    }, props.duration);
  }
});

function closeToast() {
  if (timeoutId) clearTimeout(timeoutId);
  visible.value = false;
  setTimeout(() => emit('close'), 300);
}
</script>

<template>
  <Transition name="slide-fade">
    <div v-if="visible" :class="['base-toast', `type-${type}`]" role="alert" aria-live="assertive">
      <div class="toast-content">
        <span class="toast-icon" aria-hidden="true">{{ type === 'success' ? '✓' : '!' }}</span>
        <span class="toast-message">{{ message }}</span>
      </div>
      <button class="toast-close" @click="closeToast" aria-label="Close notification">&times;</button>
    </div>
  </Transition>
</template>

<style scoped>
.base-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 2000;
  min-width: 280px;
  max-width: 400px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-left: 4px solid var(--primary-color);
}

.type-success {
  border-left-color: var(--primary-color);
}

.type-success .toast-icon {
  background: var(--primary-color);
}

.type-error {
  border-left-color: var(--error-color);
}

.type-error .toast-icon {
  background: var(--error-color);
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.toast-icon {
  width: 20px;
  height: 20px;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
  flex-shrink: 0;
}

.toast-message {
  font-size: 0.875rem;
  color: var(--text-primary);
  word-break: break-word;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--text-secondary);
  line-height: 1;
  padding: 4px;
  margin-left: 0.5rem;
  flex-shrink: 0;
  border-radius: 4px;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.05);
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

@media (max-width: 480px) {
  .base-toast {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
    min-width: auto;
    max-width: none;
  }
}
</style>