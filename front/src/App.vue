<template>
    <v-app>
        <v-app-bar
                app
                color="#ff928f"
                dark
                shrink-on-scroll
                prominent
                src="./assets/salameche.jpg"
                fade-img-on-scroll
        >
            <template v-slot:img="{ props }">
                <v-img
                        v-bind="props"
                        gradient="to top right, rgba(255,146,143,.9), rgba(255,255,255,.2)"
                ></v-img>
            </template>

            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title style="width: 30%">
                <v-row no-gutters>
                    <v-col cols="1" align-self="center">
                        <v-img
                                src="./assets/logo.png"
                                aspect-ratio="1"
                                max-width="30"
                        ></v-img>
                    </v-col>
                    <v-col cols="11">
                        <span class="headline font-weight-bold">Pokedex</span>
                    </v-col>
                </v-row>
            </v-toolbar-title>

            <div class="flex-grow-1"></div>

            <v-slide-x-transition>
                <v-text-field
                        v-if="searchAvailable"
                        class="mr-2"
                        label="Search ..."
                        prepend-inner-icon="search"
                        v-model="search"
                        clearable
                        single-line
                        light
                        solo
                >
                </v-text-field>
            </v-slide-x-transition>

            <v-btn icon>
                <v-icon @click="searchAvailable = !searchAvailable">mdi-magnify</v-icon>
            </v-btn>

            <v-btn icon>
                <v-icon>mdi-heart</v-icon>
            </v-btn>

            <v-btn icon>
                <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>

            <template v-slot:extension>
                <v-tabs
                        align-with-title
                        background-color="transparent"
                >
                    <v-tab>Pokemons</v-tab>
                    <v-tab>Items</v-tab>
                    <v-tab>Games</v-tab>
                </v-tabs>
            </template>
        </v-app-bar>

        <v-content>
            <v-container>
                <pokemon-list :search="search"></pokemon-list>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
    import PokemonList from "./components/PokemonList";

    export default {
        name: 'App',
        components: {
            PokemonList,
        },
        data: () => ({
            searchAvailable: false,
            search: null,
        })
    };
</script>
