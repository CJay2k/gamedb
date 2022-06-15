<script setup>
defineProps(['mainMedia'])
</script>

<template>
    <video v-if="mainMedia?.type === 'video'" class="rounded-md aspect-video" controls autoplay muted>
        <source :src="mainMedia?.src">
    </video>
    <iframe v-else-if="mainMedia?.type === 'youtube'" class="rounded-md aspect-video"
        :src="mainMedia?.src + '?rel=0&autoplay=1&mute=1&vq=hd720'" title="YouTube video player" allowfullscreen>
    </iframe>
    <img v-else class="rounded-md w-full" :src="mainMedia?.src" alt="Główny zrzut ekranu">
</template>