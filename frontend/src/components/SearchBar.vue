<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const searchQuery = ref('')

function handleSearch() {
  router.push({ name: 'search', query: { q: searchQuery.value } })
}
</script>

<template>
  <div class="flex py-14 text-pink-500 dark:text-pink-400">
    <div class="flex justify-center w-full mx-2">
      <div
        class="flex max-w-screen-sm w-full border focus-within:ring-1 rounded relative bg-gray-300 border-gray-300 dark:bg-gray-700 dark:border-gray-700 ring-pink-400 focus-within:border-pink-400">
        <label for="search_input" class="hidden">Pasek wyszukiwania</label>
        <input type="text" id="search_input" name="q" autocomplete="off" placeholder="Wyszukaj..." v-model="searchQuery"
          @keypress.enter="handleSearch()"
          class="pl-4 py-2 w-full bg-transparent border-0 focus:outline-none focus:ring-0">
        <button @click="handleSearch()" class="pr-2 py-2 focus:outline-none text-gray-100">
          <img src="@/assets/svg/search_icon.svg" alt="Wyszukaj" class="w-6 h-6" />
        </button>

      </div>
    </div>
  </div>
</template>

<style scoped>
</style>