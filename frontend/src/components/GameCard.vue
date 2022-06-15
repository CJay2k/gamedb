<script setup>
defineProps({
  gameDetails: Object,
})
</script>


<template>
  <RouterLink :to="{ name: 'game', params: { slug: gameDetails.slug } }"
    class="flex flex-col filter rounded-md overflow-hidden z-0 transition duration-300 bg-gray-200 hover:brightness-90 dark:bg-gray-800 dark:hover:brightness-125">
    <div class="h-32 bg-cover bg-top relative" :style="{ 'background-image': 'url(' + gameDetails.thumbnail + ')' }">
      <!-- <div class="flex gap-1 bg-opacity-85 w-max p-1 absolute bottom-1 right-1 rounded bg-gray-200 dark:bg-gray-800">
        {% if average_review %}
            <div class="text-pink-400 h-5 w-5">{% svg 'star' %}</div>
            <div class="text-sm leading-none my-auto">
                <div class="font-bold">{{ average_review }}</div>
            </div>
        {% else %}
            <div class="text-gray-400 h-5 w-5">{% svg 'star' %}</div>
            <div class="text-sm leading-none  my-auto">
                <div class="font-bold">Brak</div>
            </div>
        {% endif %}
      </div> -->
    </div>

    <div class="flex flex-col flex-1 justify-between p-2">
      <div class="font-bold">{{ gameDetails.title }}</div>
      <div class="py-2">
        <div class="flex h-10 gap-2">
          <!-- {% for store in game %} -->
          <div class="w-10 my-auto">
            <!-- {% if store.store_name == "Steam" %}
                {% svg 'steam_logo' %}
            {% elif store.store_name == "Epic Games" %}
                {% svg 'epic_games_logo' %}
            {% elif store.store_name == "GOG" %}
                {% svg 'gog_logo' %}
            {% elif store.store_name == "Ubisoft" %}
                {% svg 'ubisoft_logo' %}
            {% elif store.store_name == "Origin" %}
                {% svg 'origin_logo' %}
            {% elif store.store_name == "Battlenet" %}
                {% svg 'battlenet_logo' %}
            {% elif store.store_name == "PlayStation Store" %}
                {% svg 'playstation_logo' %}
            {% elif store.store_name == "Nintendo Store" %}
                {% svg 'nintendo_logo' %}
            {% elif store.store_name == "Humble Bundle" %}
                {% svg 'humble_bundle_logo' %}
            {% endif %} -->
          </div>
          <!-- {% endfor %} -->
        </div>
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
</style>
