<script setup>
defineProps({
  title: String,
  subtitle: String
});
</script>

<template>
  <div class="base-card">
    <div v-if="title || subtitle" class="card-header">
      <h3 v-if="title">{{ title }}</h3>
      <p v-if="subtitle" class="card-subtitle">{{ subtitle }}</p>
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.base-card {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: white;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.card-subtitle {
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.card-body {
  padding: 1.5rem;
}

@media (max-width: 768px) {
  .card-header, .card-body {
    padding: 1rem;
  }
}

.card-footer {
  padding: 1.25rem 1.5rem;
  background: var(--hover-bg);
  border-top: 1px solid var(--border-color);
}
</style>
