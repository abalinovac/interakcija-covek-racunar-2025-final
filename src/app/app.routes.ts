import { Routes } from '@angular/router';
import { Home } from './home/home';
import { About } from './about/about';
import { Details } from './details/details';
import { Login } from './login/login';
import { Singup } from './singup/singup';

export const routes: Routes = [
    {path: '', component: Home, title: 'Home' },
    {path: 'about', component: About, title: 'About'},
    {path: 'details/:id', component: Details, title: 'Details'},
    {path: 'login', component: Login, title: 'Login'},
    {path: 'singup', component: Singup, title: 'Singup'},
    {path: '**', redirectTo: '' }
];
