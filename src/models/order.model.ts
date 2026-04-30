export interface OrderModel{
    orderId: string,
    toyId: number,
    toyName: string,
    time: string,
    quantity: number,
    status: 'na' | 'paid' | 'canceled' | 'liked' | 'disliked'
}