import { Component, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { UserService } from '../services/user.service';
import { Utils } from './utils';
import Swal from 'sweetalert2';
import { MessageModel } from '../models/message.model';
import { RasaService } from '../services/rasa.service';
import { FormsModule } from '@angular/forms';

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

  sendUserMessage() {
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

    RasaService.sendMessage(trimmedMessage).then(rsp => {
      if (rsp.data.length == 0) {
        this.messages.push({
          type: 'bot',
          text: 'Sorry, I didnt undrestand that.'
        })

        return
      }

      for (let botMessage of rsp.data)
        this.messages.push({
          type: 'bot',
          text: botMessage.text
        })
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
