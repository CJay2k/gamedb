<template>
  <nav class="flex items-center justify-between max-w-7xl w-full h-12 select-none gap-2">
    <div class="px-2 xl:px-0">
      <RouterLink :to="{ name: 'home' }">
        <div class="flex items-center w-12 h-12">
          <img src="@/assets/logo.svg" alt="GameDB Logo" />
        </div>
      </RouterLink>
    </div>

    <!-- search bar -->

    <div class="block h-full">
      <div class="flex h-full items-stretch">
        <div onclick="toggle_dark_mode()"
          class="w-10 cursor-pointer my-auto p-2 ml-2 sm:ml-0 hover:bg-gray-300 dark:hover:bg-gray-700 rounded-md transition-colors duration-150">
          <div class="w-full h-full hidden dark:block">
            <img src="@/assets/svg/sun.svg" alt="GameDB Logo" />
          </div>
          <div class="w-full h-full dark:hidden transform -rotate-90">
            <img src="@/assets/svg/moon.svg" alt="GameDB Logo" />
          </div>
        </div>
        <nav id="menu"
          class="fixed hidden md:flex top-12 left-0 flex-col w-full text-center h-screen md:h-auto bg-opacity-95 dark:bg-opacity-90 bg-gray-200 dark:bg-black p-4 gap-4 md:gap-0 md:static md:flex-row md:pt-3 md:p-0 md:bg-transparent md:dark:bg-transparent">
          <RouterLink :to="{ name: 'home' }" id="index" class="navbar-item-link w-full md:w-max">Strona
            główna</RouterLink>
          <RouterLink :to="{ name: 'search' }" id="search" class="navbar-item-link w-full md:w-max">
            Wyszukiwarka
          </RouterLink>

          <!-- <RouterLink to="/"> id="stats" class="navbar-item-link w-full md:w-max">Rankingi</RouterLink> -->

          <!-- if user is authenticated 
          <a id="profile" class="navbar-item-link w-full md:w-max" href="{% url 'game_finder:profile' %}">Profil</a>

          else
          <a id="profile" class="navbar-item-link w-full md:w-max" href="{% url 'account_login' %}">Zaloguj</a>
          -->
        </nav>
      </div>
    </div>

    <div class="items-center md:hidden">
      <button type="button" onclick="toggle_hamburger_menu()" class="flex items-center w-12 px-2 focus:outline-none">
        <img src="@/assets/svg/hamburger_menu.svg" />
      </button>
    </div>
  </nav>
</template>


<style scoped>
.navbar-item-link {
  @apply px-4 border-b-4 border-transparent font-semibold duration-300;
}

.navbar-item-link.active,
.navbar-item-link:hover {
  @apply font-semibold text-pink-600;
}

@screen md {
  .navbar-item-link:hover {
    @apply border-pink-600
  }
}
</style>