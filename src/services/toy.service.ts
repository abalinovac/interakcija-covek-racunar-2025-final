import axios from "axios";
import { ToyModel } from "../models/toy.model";
import { AgeModel } from "../models/age.model";

const client = axios.create({
    baseURL: 'https://toy.pequla.com/api',
    headers: {
        'Accept': 'application/json',
        'X-Name': 'ICR/2025'
    }
})

export class ToyService{
    static async getToys(search: string = '', age: number = 0){
       return client.request<ToyModel[]>({
        url: '/toy',
        method: 'get',
        params: {
            'search': search,
            'age': age
        }
       })
    }

    static async getToyByPermalink(permalink: string){
        return client.get<ToyModel>(`/toy/permalink/${permalink}`)
    }

    static async getAgeGroup(){
        return client.get<AgeModel[]>(`/age-group`)
    }
}