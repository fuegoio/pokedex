<template>
    <v-slide-y-transition
            mode="in-out"
            class="row py-2"
            group
            tag="div"
    >
        <v-col cols="6" v-for="pokemon in pokemons" :key="pokemon.name">
            <Pokemon :pokemon="pokemon" @delete="deletePokemon(pokemon)"
                     @update="updatePokemon(pokemon)"/>
        </v-col>
    </v-slide-y-transition>
</template>

<script>
    import axios from 'axios';
    import Pokemon from './Pokemon';

    export default {
        name: "PokemonList",
        props: ['search'],
        data: () => ({
            pokemons: []
        }),
        components: {
            Pokemon,
        },
        watch: {
            search() {
                this.searchPokemons();
            }
        },
        created() {
            this.searchPokemons();
        },
        methods: {
            searchPokemons() {
                let search = this.search;
                if (!search) {
                    search = "";
                }

                let params = {query: search};
                axios.get('http://localhost:8000/api/v1/pokemons', {params: params}).then((response) => {
                    this.pokemons = response.data;
                });
            },
            updatePokemon(pokemon) {
                axios.get('http://localhost:8000/api/v1/pokemon/' + pokemon.name).then((response) => {
                    let index_of_pokemon = this.pokemons.indexOf(pokemon);

                    let new_pokemon = response.data;
                    this.pokemons.splice(index_of_pokemon, 1, new_pokemon);
                });
            },
            deletePokemon(pokemon) {
                let index_of_pokemon = this.pokemons.indexOf(pokemon);
                this.pokemons.splice(index_of_pokemon, 1);
            }
        }
    }
</script>

<style scoped>

</style>