<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <header class="flex justify-center w-full bg-primary-200 fixed z-50">
    <NavBar />
  </header>

  <main class="flex justify-center w-full pt-12 px-2 mb-2">
    <div class="w-full max-w-screen-xl relative">
      <RouterView />
    </div>
  </main>
</template>

<style>
@import "@/assets/base.css";
</style>
