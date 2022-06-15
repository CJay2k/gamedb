<script setup>
import GameCard from './GameCard.vue';

defineProps({
  foundGames: Object
})
</script>

<template>
  <div v-if="foundGames.status === 200"
    class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 auto-rows-fr">
    <GameCard v-for="(game, index) in foundGames.data" :key="index" :gameDetails="game" />
  </div>
</template>

<style scoped>
</style>
