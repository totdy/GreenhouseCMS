<script lang="ts" setup>
import { onMounted } from 'vue';

const props = defineProps({
    type: {
        type: String,
        required: true,        
    },
    msg: {
        type: String,
        required: true,        
    },
})

const emit = defineEmits(["close"])

onMounted(() => {
    setTimeout(() => emit("close"), 3000)
})

</script>

<template>
    <div :class="props.type">
        <p>{{ props.msg }}</p>
    </div>
</template>

<style lang="css" scoped>
div {
    display: flex;
    justify-content: center;

    position: fixed;
    top: 0;
    left: 0;

    width: 100%;

    padding: 1rem;
}
.info {
    background-color: var(--info);
}

.warning {
    background-color: var(--warning);
}

.success {
    background-color: var(--success);
}

.error {
    background-color: var(--danger);
}
</style>