import { Routes } from '@angular/router';
import { Home } from './home/home';
import { About } from './about/about';
import { Login } from './login/login';
import { Singup } from './singup/singup';
import { Movie } from './movie/movie';

export const routes: Routes = [
    {path: '', component: Home, title: 'Home' },
    {path: 'about', component: About, title: 'About'},
    {path: 'movie/:path', component: Movie, title: 'Movie'},
    {path: 'login', component: Login, title: 'Login'},
    {path: 'singup', component: Singup, title: 'Singup'},
    {path: '**', redirectTo: '' }
];
