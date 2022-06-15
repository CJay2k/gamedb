<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import API from '../api';
import MainMedia from '../components/gameDetails/MainMedia.vue';
import Description from '../components/gameDetails/Description.vue';
import Gallery from '../components/gameDetails/Gallery.vue';
import InfoCard from '../components/gameDetails/InfoCard.vue';

const gameDetails = ref({})
const route = useRoute()

API
  .get(route.path)
  .then(response => (gameDetails.value = response))
  .then(() => {
    const images = gameDetails.value.data.images
    if (images.length % 3 === 2) {
      gameDetails.value.data.images = images.slice(0, images.length - 1)
    }
  })
  .catch(error => console.log(error))
</script>

<template>
  <h1 class="text-2xl md:text-4xl lg:text-5xl py-2 text-gray-900 dark:text-gray-100">{{ gameDetails?.data?.title }}
  </h1>
  <div class="w-full">
    <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900"></div>
  </div>

  <!-- {% if failed_to_load %}
  <div class="py-1 mt-2 px-2 mx-4 text-gray-2 bg-opacity-90 font-bold rounded text-gray-100 bg-red-600">
    Wystąpił błąd podczas ładowania danych ze sklep{{ failed_to_load | pluralize: "u,ów" }}: {{ failed_to_load | join: ", " }}
  </div>
  {% endif %} -->
  <div class="flex flex-col-reverse md:flex-row  xl:px-0 py-2">
    <div class="flex flex-1 flex-col text-gray-600 dark:text-gray-300">
      <MainMedia :mainMedia="gameDetails?.data?.main_media" />
      <Description :description="gameDetails?.data?.description" />
      <Gallery :images="gameDetails?.data?.images" />
    </div>
    <InfoCard :gameDetails="gameDetails?.data" />
  </div>

</template>

<style>
</style>
