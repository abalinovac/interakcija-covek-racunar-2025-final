export interface RasaModel {
    text: string
    attachment: {
        type: 'toy_list' | 'single_toy' | 'age_list' | 'actor_list' | 'director_list' | 'order_toy' | 'simple_list' | 'create_order'
        data: any
    }
}