<script setup>
import { onMounted } from "vue";
import { useUsers } from "./composables/useUsers";

const { users, fetchUsers } = useUsers();

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <router-view />
</template>