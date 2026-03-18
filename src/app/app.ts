import { Component, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { UserService } from '../services/user.service';
import { Utils } from './utils';
import Swal from 'sweetalert2';
import { MessageModel } from '../models/message.model';
import { RasaService } from '../services/rasa.service';
import { FormsModule } from '@angular/forms';
import { MovieService } from '../services/movie.service';
import { MovieModel } from '../models/movie.model';
import { AxiosResponse } from 'axios';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected year = new Date().getFullYear()
  protected waitingForResponse: boolean = false
  protected botThinkingPlaceholder: string = 'Thinking...'
  protected isChatVisible: boolean = false
  protected userMessage: string = ''
  protected messages: MessageModel[] = []
  msg: any;

  constructor(private router: Router, private utils: Utils) {
    this.messages.push({
      type: 'bot',
      text: 'How can I help you..?'
    })

  }

  toggleChat() {
    this.isChatVisible = !this.isChatVisible
  }

  async sendUserMessage() {
    if (this.waitingForResponse) return

    const trimmedMessage = this.userMessage.trim()
    this.userMessage = ''

    this.messages.push({
      type: 'user',
      text: trimmedMessage
    })

    this.messages.push({
      type: 'bot',
      text: this.botThinkingPlaceholder
    })

    //RasaService.sendMessage(trimmedMessage).then(rsp => {
    //  if (rsp.data.length == 0) {
    //    this.messages.push({
    //      type: 'bot',
    //      text: 'Sorry, I didnt undrestand that.'
    //    })
    //
    //    return
    //  }
    //
    //  for (let botMessage of rsp.data) {
    //    this.messages.push({
    //      type: 'bot',
    //      text: botMessage.text
    //    })
    //  }
    //
    //  this.messages = this.messages.filter(m => {
    //    if (m.type === 'bot') {
    //      return m.text != this.botThinkingPlaceholder
    //    }
    //
    //    return true
    //  })
    //})


    //Primer bez RASA
    if (trimmedMessage.includes('movies')) {
      await this.createBotResponseAsMovieList()
      return
    }

    const genres = await MovieService.getGenres()
    if (trimmedMessage.includes('genre list')) {
      let html = `<ul class="list-unstyled">`
      genres.data.map(g => `<li>${g.name}</li>`)
        .forEach(g => html += g)
      html += `</ul>`

      this.messages.push({
        type: 'bot',
        text: html
      })
      this.removeBotPlaceholder()
      return
    }

    //napravi odg bota za sve zanrove da vrati filmove 
    for (let genre of genres.data) {
      if (trimmedMessage.includes('genre' + genre.name.toLowerCase())) {
        await this.createBotResponseAsMovieList(genre.genreId)
        return
      }
    }

    this.removeBotPlaceholder()
    this.messages.push({
        type: 'bot',
        text: 'Seams like cant help you with that..'
      })
  }

  async createBotResponseAsMovieList(genre: number = 0) {
    const movies = await MovieService.getMovies('', genre)

    let html = `<ul class="list-unstyled">`
    movies.data.map(m => `<li><a href="/movie/${m.shortUrl}">${m.title} (${m.director.name})</a></li>`)
      .forEach(m => html += m)
    html += `</ul>`

    this.messages.push({
      type: 'bot',
      text: html
    })
    this.removeBotPlaceholder()
  }

  removeBotPlaceholder() {
    this.messages = this.messages.filter(m => {
      if (m.type === 'bot') {
        return m.text != this.botThinkingPlaceholder
      }
      return true
    })
  }

  getUserName() {
    const user = UserService.getActiveUser()
    return `${user.firstname} ${user.lastname}`
  }

  hasAuth() {
    return UserService.hasAuth()
  }

  doLogout() {
    this.utils.showDialog(
      "Are you sure you want to logout?", () => {
        UserService.logout()
        this.router.navigateByUrl('/login')
      },
      "Logout now",
      "Don't Logout"
    )
  }
}
