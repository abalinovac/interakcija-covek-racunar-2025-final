import { Routes } from '@angular/router';
import { Home } from './home/home';
import { About } from './about/about';
import { Login } from './login/login';
import { Movie } from './movie/movie';
import { Profile } from './profile/profile';
import { Reservation } from './reservation/reservation';

 

export const routes: Routes = [
    {path: '', component: Home, title: 'Home' },
    {path: 'about', component: About, title: 'About'},
    {path: 'movie/:path/reservation', component: Reservation, title: 'Movie reservation'},
    {path: 'movie/:path', component: Movie, title: 'Movie'},
    {path: 'login', component: Login, title: 'Login'},
    {path: 'profile', component: Profile, title: 'User profile'},
    {path: '**', redirectTo: '' }
];
