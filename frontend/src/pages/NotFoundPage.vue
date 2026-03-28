<template>
    <div class="not-found-container">
        <div class="not-found-content">
            <h1 class="not-found-code">404</h1>
            <h2 class="not-found-title">Page Not Found</h2>
            <p class="not-found-message">
                The page you are looking for doesn't exist or has been moved.
            </p>
            <BaseButton variant="primary" @click="goHome">
                Go to Dashboard
            </BaseButton>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import BaseButton from "../components/base/BaseButton.vue";

const router = useRouter();

function goHome() {
    router.push("/dashboard");
}
</script>

<style scoped>
.not-found-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-color, #f5f5f5);
    padding: 2rem;
}

.not-found-content {
    text-align: center;
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
}

.not-found-code {
    font-size: 6rem;
    font-weight: 700;
    margin: 0;
    color: var(--primary-color, #008a00);
    line-height: 1;
}

.not-found-title {
    font-size: 1.5rem;
    margin: 1rem 0;
    color: var(--text-primary, #1a1a1a);
}

.not-found-message {
    color: var(--text-secondary, #666);
    margin-bottom: 2rem;
}

@media (max-width: 480px) {
    .not-found-content {
        padding: 2rem;
    }

    .not-found-code {
        font-size: 4rem;
    }

    .not-found-title {
        font-size: 1.25rem;
    }
}
</style>