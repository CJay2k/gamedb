<script setup>
import { onMounted, watch } from 'vue';
import SearchResults from '../components/SearchResults.vue';
import { ref } from 'vue';
import API from '../api.js'
import { useRoute } from 'vue-router';
import SearchBar from '../components/SearchBar.vue';

const foundGames = ref([])
const route = useRoute();

watch(route, () => {
  API
    .get('search/', { params: route.query })
    .then(response => (foundGames.value = response))
    .catch(error => console.log(error))
}, { immediate: true })

</script>

<template>
  <SearchBar />
  <div>
    <SearchResults :foundGames='foundGames' />
  </div>
</template>

<style>
</style>
