export interface RasaModel {
    text: string
    attachment: {
        type: 'movie_list' | 'single_movie' | 'genre_list' | 'actor_list' | 'director_list' | 'simple_list' | 'create_order'
        data: any
    }
}