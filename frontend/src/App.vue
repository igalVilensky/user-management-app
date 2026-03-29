<script setup>
import { onMounted } from "vue";
import { useUsers } from "./composables/useUsers";

const { users, fetchUsers } = useUsers();

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <!-- Skip to main content link for keyboard users -->
  <a href="#main-content" class="skip-to-content">
    Skip to main content
  </a>

  <!-- Main content with ID for skip link -->
  <main id="main-content" tabindex="-1">
    <router-view />
  </main>
</template>

<style>
.skip-to-content {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary-color, #008a00);
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 9999;
  border-radius: 0 0 4px 0;
  font-family: inherit;
  font-size: 14px;
}

.skip-to-content:focus {
  top: 0;
  outline: 2px solid white;
  outline-offset: 2px;
}

/* Ensure main content can receive focus without visible outline */
#main-content:focus {
  outline: none;
}
</style>