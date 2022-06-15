<script setup>
defineProps(['images'])
</script>

<template>
    <div class="font-bold">Zrzuty ekranu:</div>
    <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900"></div>
    <div id="gallery_container" class="flex flex-wrap p-2 pb-1 overflow-hidden transition-all duration-500">
        <div v-for="(image, index) in images" class="py-1"
            :class="{ 'w-full': index % 3 === 0, 'w-1/2 pr-1': index % 3 === 1, 'w-1/2 pl-1': index % 3 === 2 }">
            <img class="rounded-md w-full h-full object-cover" :src="image" alt="Zrzut ekranu">
        </div>
    </div>

    <!-- <div id="gallery_show_more_less"
        class="hidden justify-center py-1 mb-2 mx-2 cursor-pointer rounded-md select-none relative bg-gray-200 hover:bg-gray-300 text-pink-600 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-pink-400">
        <div class="font-bold">POKAŻ WIĘCEJ</div>
        <div class="transform duration-500 my-auto w-3 ml-1">
            <img src="@/assets/svg/arrow_down.svg" alt="V" />
        </div>
        <div class="absolute w-full h-28 -top-28 bg-gradient-to-b from-transparent to-gray-100 dark:to-gray-900"></div>
    </div> -->
</template>