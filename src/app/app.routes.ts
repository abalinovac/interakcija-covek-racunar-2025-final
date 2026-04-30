import { Routes } from '@angular/router';
import { Home } from './home/home';
import { About } from './about/about';
import { Login } from './login/login';
import { Toy } from './toy/toy';
import { Profile } from './profile/profile';
import { Reservation } from './reservation/reservation';

 

export const routes: Routes = [
    {path: '', component: Home, title: 'Home' },
    {path: 'about', component: About, title: 'About'},
    {path: 'toy/:path/reservation', component: Reservation, title: 'Toy reservation'},
    {path: 'toy/:path', component: Toy, title: 'Toy'},
    {path: 'login', component: Login, title: 'Login'},
    {path: 'profile', component: Profile, title: 'User profile'},
    {path: '**', redirectTo: '' }
];
