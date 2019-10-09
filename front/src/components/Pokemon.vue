<template>
    <div class="pokemon">
        <v-card class="mx-auto" hover>
            <v-list-item three-line>
                <v-list-item-content>
                    <v-list-item-title class="display-1 text--primary mb-1">{{ pokemon.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ pokemon.stats }}</v-list-item-subtitle>
                </v-list-item-content>


                <v-list-item-avatar
                        tile
                        size="80"
                >
                    <v-img
                            :src="pokemon.sprite_front"
                            aspect-ratio="1"
                    ></v-img>
                </v-list-item-avatar>
            </v-list-item>

            <v-card-actions>
                <v-chip v-for="type in pokemon.types" class="mx-1" :key="type">{{ type }}</v-chip>
                <v-spacer></v-spacer>
                <v-btn text icon color="blue" @click="startEditPokemon">
                    <v-icon>edit</v-icon>
                </v-btn>
                <v-btn text icon color="red" @click="deletePokemon">
                    <v-icon>delete</v-icon>
                </v-btn>
            </v-card-actions>
        </v-card>

        <v-row justify="center">
            <v-dialog v-model="edit" persistent max-width="600px">
                <v-card v-if="pokemon_edited">
                    <v-card-title class="mb-1">
                        <span class="display-1">{{ pokemon.name }}</span>
                    </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" md="4" v-for="stat in Object.keys(pokemon_edited.stats)" :key="stat">
                                    <v-text-field
                                            :label="stat"
                                            v-model="pokemon_edited.stats[stat]"
                                            outlined
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-select
                                            v-model="pokemon_edited.types"
                                            :items="types"
                                            chips
                                            label="Types"
                                            multiple
                                            outlined
                                    ></v-select>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>
                    <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn color="grey darken-1" text @click="edit = false">Close</v-btn>
                        <v-btn color="primary" @click="editPokemon">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        props: ['pokemon'],
        data: () => ({
            edit: false,
            pokemon_edited: null,
            types: null
        }),
        methods: {
            startEditPokemon() {
                this.types = [];
                this.pokemon_edited = {
                    stats: {},
                    types: []
                };
                Object.keys(this.pokemon.stats).forEach((stat) => {
                    this.pokemon_edited.stats[stat] = this.pokemon.stats[stat];
                });
                this.pokemon.types.forEach((type) => {
                    this.pokemon_edited.types.push(type);
                    this.types.push(type);
                });

                axios.get('http://localhost:8000/api/v1/types').then((response) => {
                    this.types = response.data;
                });

                this.edit = true;
            },
            editPokemon() {
                axios.patch('http://localhost:8000/api/v1/pokemon/' + this.pokemon.name, this.pokemon_edited).then(() => {
                    this.$emit('update');
                }).catch(() => {
                    console.log('error');
                });
                this.edit = false;
            },
            deletePokemon() {
                axios.delete('http://localhost:8000/api/v1/pokemon/' + this.pokemon.name).then(() => {
                    this.$emit('delete');
                });
            }
        }
    };
</script>
