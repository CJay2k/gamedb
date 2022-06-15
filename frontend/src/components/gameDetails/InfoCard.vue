<script setup>
defineProps(['gameDetails'])
</script>

<template>
    <div class="w-full md:w-80 mb-5 md:ml-7 text-gray-900 dark:text-gray-100">
        <div class="sticky top-20">
            <div class="w-full max-h-60 bg-cover bg-clip-content bg-no-repeat rounded-md"
                :style="{ 'background-image': 'url(' + gameDetails?.thumbnail + ')' }">
                <img class="invisible w-full" :src="gameDetails?.thumbnail" alt="Miniaturka" />
            </div>
            <div class="pt-2 flex justify-between items-center">
                <div class="font-bold">Gra jest dostępna w sklepach:</div>
            </div>
            <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900">
            </div>

            <div class="grid grid-cols-4 auto-rows-fr p-2">

                <a v-for="store in gameDetails.stores" class="w-full" :href="store.game_url">
                    <div class="flex flex-col items-center h-full">
                        <div class="flex flex-wrap-reverse justify-center items-start p-1 w-full flex-1">
                            <span class="flex font-bold w-max h-8 p-1 text-center items-center text-sm platform-svg"
                                style="max-width: 2rem;">
                                <img class="w-8" v-if="store.store_name === 'Battlenet'"
                                    src="@/assets/svg/battlenet_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'Epic Games'"
                                    src="@/assets/svg/epic_games_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'GOG'" src="@/assets/svg/gog_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'Origin'"
                                    src="@/assets/svg/origin_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'PlayStation Store'"
                                    src="@/assets/svg/playstation_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'Steam'"
                                    src="@/assets/svg/steam_logo.svg" />
                                <img class="w-8" v-if="store.store_name === 'Ubisoft'"
                                    src="@/assets/svg/ubisoft_logo.svg" />
                            </span>
                        </div>
                        <span v-if="store.price === 0" class="text-sm mt-1">


                            Darmowa

                        </span>

                        <span v-else> {{ store.price }}zł</span>
                    </div>
                </a>
                <!-- {% endfor %} -->
            </div>

            <!-- <div class="font-bold">Oceny użytkowników:</div>
            <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900">
            </div>
            <div class="flex h-12 p-2">
                <div class="h-8 w-8 text-pink-400">{% svg 'star' %}</div>
                {% if reviews_count %}
                <div class="font-bold text-3xl leading-none ml-2 text-gray-900 dark:text-gray-100">{{ reviews_average }}
                </div>
                <div class="pl-2 text-xs leading-none my-auto text-gray-700 dark:text-gray-300">
                    <div>{{ reviews_count | intword }}</div>
                    <div>ocen{{ reviews_count | pluralize: "a," }}</div>
                </div>
                {% else %}
                <div class="font-bold text-xl leading-none my-auto ml-2 text-gray-900 dark:text-gray-100">Brak ocen
                </div>
                {% endif %}

            </div>
            {% if user.is_authenticated %}
            <div class="flex justify-between pr-1">
                <div class="font-bold">Twoja ocena:</div>

                <form id="favorite_form"
                    class="h-6 w-6 transition-all ease-in-out duration-300 cursor-pointer hover:text-pink-400 dark:hover:text-pink-400 text-gray-300 dark:text-gray-700"
                    action="" method="post">
                    {% csrf_token %}
            <button id="favorite_button" type="submit" name="favorite" value="toggle"
                class="focus:outline-none focus:ring-0 w-6">{% svg 'heart' %}</button>
            </form>
        </div> -->

            <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900">
            </div>

            <!-- <form id="rating_form" class="flex flex-row-reverse h-14 text-gray-300 dark:text-gray-700" action=""
                method="post">
                {% csrf_token %}
                <button type="submit" name="vote" value="10">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="9">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="8">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="7">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="6">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="5">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="4">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="3">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="2">{% svg 'star' %}</button>
                <button type="submit" name="vote" value="1">{% svg 'star' %}</button>
            </form> -->
            <!-- {% else %} -->
            <!-- <div class="font-bold">Dodaj do ulubionych/oceń grę</div>
            <div class="font-bold"><a class="text-pink-600 dark:text-pink-400"
                    href="{% url 'account_login' %}?next=/game/{{ slug }}">Zaloguj się </a>by wykonać te czynności</div>
            <div class="w-full h-px bg-gradient-to-r from-gray-400 to-gray-100 dark:from-gray-600 dark:to-gray-900">
            </div> -->
            <!-- {% endif %} -->
        </div>
    </div>
</template>