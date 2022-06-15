<script setup>
defineProps(['description'])
</script>

<template>
    <div class="font-bold py-2">Opis gry:</div>
    <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900"></div>
    <div id="about" class="p-2 overflow-hidden transition-all duration-500" v-html="description"></div>

    <!-- <div id="about_game_show_more_less"
        class="hidden justify-center py-1 mb-2 mx-2 cursor-pointer rounded-md select-none relative bg-gray-200 hover:bg-gray-300 text-pink-600 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-pink-400">
        <div class="font-bold">POKAŻ WIĘCEJ</div>
        <div class="transform duration-500 my-auto w-3 ml-1">
            <img src="@/assets/svg/arrow_down.svg" />
        </div>
        <div class="absolute w-full h-28 -top-28 bg-gradient-to-b from-transparent to-gray-100 dark:to-gray-900"></div>
    </div> -->
</template>

<style scoped>
#about h1,
#about h2,
#about h3 {
    @apply mt-4 font-bold;
}

#about :deep(img) {
    @apply w-full rounded-md inline-block;
}

#about ul {
    @apply inline-block list-disc pl-4 mb-4;
}

#about strong {
    @apply inline;
}

#about.steam strong {
    @apply block;
}

#about.steam strong+br,
#about.steam h2.bb_tag+br {
    @apply hidden;
}

#about p {
    @apply mb-4;
}
</style>