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

onMounted(() => {
  if (props.duration > 0) {
    setTimeout(() => {
      visible.value = false;
      setTimeout(() => emit('close'), 300); // Wait for transition
    }, props.duration);
  }
});
</script>

<template>
  <Transition name="slide-fade">
    <div v-if="visible" :class="['base-toast', `type-${type}`]">
      <div class="toast-content">
        <span class="toast-icon">✓</span>
        <span class="toast-message">{{ message }}</span>
      </div>
      <button class="toast-close" @click="visible = false">&times;</button>
    </div>
  </Transition>
</template>

<style scoped>
.base-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 2000;
  min-width: 300px;
  max-width: 450px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-left: 5px solid var(--primary-color);
}

.type-success {
  border-left-color: var(--primary-color);
}

.type-error {
  border-left-color: var(--error-color);
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.toast-icon {
  width: 20px;
  height: 20px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.toast-message {
  font-size: 0.875rem;
  color: var(--text-primary);
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--text-secondary);
  line-height: 1;
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
</style>
