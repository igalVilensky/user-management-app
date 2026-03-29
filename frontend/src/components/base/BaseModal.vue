<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue';

const props = defineProps({
  show: Boolean,
  title: String
});

const emit = defineEmits(['close']);

const modalContent = ref(null);

// Unique IDs for accessibility
const titleId = `modal-title-${Math.random().toString(36).slice(2)}`;
const descriptionId = `modal-desc-${Math.random().toString(36).slice(2)}`;

let previousActiveElement = null;
let isFocusTrapActive = false;

// Focus trap + ESC handling
function handleKeydown(e) {
  if (!isFocusTrapActive || !modalContent.value) return;

  // ESC closes modal
  if (e.key === 'Escape') {
    e.preventDefault();
    emit('close');
    return;
  }

  const focusableElements = modalContent.value.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  if (focusableElements.length === 0) return;

  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstFocusable) {
      e.preventDefault();
      lastFocusable.focus();
    } else if (!e.shiftKey && document.activeElement === lastFocusable) {
      e.preventDefault();
      firstFocusable.focus();
    }
  }
}

// Handle focus when modal opens
async function handleModalOpen() {
  previousActiveElement = document.activeElement;

  await nextTick();

  if (modalContent.value) {
    isFocusTrapActive = true;

    const focusableElements = modalContent.value.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const autofocusEl = modalContent.value.querySelector('[autofocus]');
    const firstInput = modalContent.value.querySelector('input, textarea, select');

    setTimeout(() => {
      if (autofocusEl) autofocusEl.focus();
      else if (firstInput) firstInput.focus();
      else if (focusableElements.length > 0) focusableElements[0].focus();
      else modalContent.value.focus();
    }, 10);
  }

  document.addEventListener('keydown', handleKeydown);

  // Prevent background scroll
  document.body.style.overflow = 'hidden';

  // Optional: prevent interaction with background
  document.querySelector('#app')?.setAttribute('inert', '');
}

// Handle focus when modal closes
function handleModalClose() {
  isFocusTrapActive = false;

  document.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';

  document.querySelector('#app')?.removeAttribute('inert');

  if (previousActiveElement && previousActiveElement.focus) {
    setTimeout(() => {
      previousActiveElement.focus();
    }, 10);
  }
}

// Watch modal visibility
watch(() => props.show, (newVal) => {
  if (newVal) {
    handleModalOpen();
  } else {
    handleModalClose();
  }
});

// Cleanup
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
  document.querySelector('#app')?.removeAttribute('inert');
});
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
        <div ref="modalContent" class="modal-content" tabindex="-1" role="dialog" aria-modal="true"
          :aria-labelledby="titleId" :aria-describedby="descriptionId">
          <header class="modal-header">
            <h3 :id="titleId">{{ title }}</h3>
            <button class="close-btn" @click="$emit('close')" aria-label="Close modal" type="button">
              &times;
            </button>
          </header>

          <div class="modal-body" :id="descriptionId">
            <slot />
          </div>

          <footer class="modal-footer">
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  max-height: 92vh;
  overflow: hidden;
  outline: none;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: var(--text-secondary);
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

.close-btn:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  flex-shrink: 0;
}

/* Mobile */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 0;
    align-items: flex-end;
  }

  .modal-content {
    max-height: 95vh;
    border-radius: 16px 16px 0 0;
    margin: 0;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>