export interface OrderModel{
    orderId: string,
    toyId: number,
    toyName: string,
    delivery: string,
    quantity: number,
    status: 'na' | 'paid' | 'canceled' | 'liked' | 'disliked'
}