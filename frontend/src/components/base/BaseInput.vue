<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  error: String,
  placeholder: String,
  type: {
    type: String,
    default: 'text'
  },
  required: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  autocomplete: String
});

defineEmits(['update:modelValue']);
</script>

<template>
  <div class="base-input-wrapper">
    <label v-if="label" :for="id" class="input-label">
      {{ label }}
      <span v-if="required" class="required-star" aria-hidden="true">*</span>
    </label>
    <input :id="id" :type="type" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
      class="base-input" :class="{ 'has-error': error }" :placeholder="placeholder" :required="required"
      :aria-invalid="!!error" :aria-describedby="error ? `${id}-error` : null" :aria-required="required"
      :autocomplete="autocomplete" />
    <span v-if="error" :id="`${id}-error`" class="input-error" role="alert">
      {{ error }}
    </span>
  </div>
</template>

<style scoped>
.base-input-wrapper {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.required-star {
  color: var(--error-color);
  margin-left: 4px;
}

.base-input {
  padding: 0.625rem 0.875rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  font-size: 1rem;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.base-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 138, 0, 0.1);
}

.base-input.has-error {
  border-color: var(--error-color);
}

.base-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(215, 0, 0, 0.1);
}

.input-error {
  color: var(--error-color);
  font-size: 0.75rem;
  margin-top: 0.25rem;
}
</style>