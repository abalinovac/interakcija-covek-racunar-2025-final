import { Component } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { UserService } from '../services/user.service';
import { Utils } from './utils';
import { MessageModel } from '../models/message.model';
import { RasaService } from '../services/rasa.service';
import { FormsModule } from '@angular/forms';
import { ToyService } from '../services/toy.service';
import { ToyModel } from '../models/toy.model';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected year = new Date().getFullYear()
  protected waitingForResponse: boolean = false
  protected botThinkingPlaceholder: string = 'Thinking ...'
  protected isChatVisible: boolean = false
  protected userMessage: string = ''
  protected messages: MessageModel[] = []

  constructor(private router: Router, private utils: Utils) {
    this.messages.push({
      type: 'bot',
      text: 'How can I help you?'
    })
  }

  toggleChat() {
    this.isChatVisible = !this.isChatVisible
  }

  async sendUserMessage() {
    if (this.waitingForResponse || !this.userMessage.trim()) return

    const trimmedMessage = this.userMessage.trim()
    this.userMessage = ''
    this.waitingForResponse = true

    // 1. Dodajemo korisničku poruku
    this.messages.push({ type: 'user', text: trimmedMessage })
    
    // 2. Dodajemo placeholder dok bot "razmišlja"
    this.messages.push({ type: 'bot', text: this.botThinkingPlaceholder })

    RasaService.sendMessage(trimmedMessage)
      .then(rsp => {
        this.removeBotPlaceholder()
        this.waitingForResponse = false

        if (rsp.data.length == 0) {
          this.messages.push({
            type: 'bot',
            text: "Sorry, I didn't understand your question!"
          })
          return
        }

        for (let message of rsp.data) {
          // PRVO: Provera attachment-a (ako postoji)
          if (message.attachment != null) {
            let html = ''

            // Slučaj: toy_list
            if (message.attachment.type == 'toy_list' && Array.isArray(message.attachment.data)) {
              for (let toy of message.attachment.data as ToyModel[]) {
                html += `<div style="border-bottom: 1px solid #444; margin-bottom: 10px; padding-bottom: 5px;">`
                html += `<ul class='list-unstyled'>`
                html += `<li><strong>Name:</strong> ${toy.name}</li>`
                html += `<li><strong>Description:</strong> ${toy.description}</li>`
                html += `<li><strong>AgeGroup:</strong> ${toy.ageGroup}</li>`
                html += `<li><strong>Price:</strong> ${toy.price}</li>`
                html += `</ul>`
                html += `<p><small>${toy.description}</small></p>`
                html += `</div>`
              }
            }

            // Slučaj: direktori, žanrovi, glumci
            else if (['age_list', 'price_list', 'director_list'].includes(message.attachment.type)) {
              html = `<ul class='list-unstyled'>`
              for (let obj of message.attachment.data) {
                html += `<li>• ${obj.name}</li>`
              }
              html += `</ul>`
            }

            //Slučaj: Napravi porudžbinu
            if(message.attachment.type = 'order_toy'){
              this.router.navigateByUrl(`/toy/${(message.attachment.data as ToyModel).toyId}/reservation`)
            }

            // Slučaj: simple_list ili create_order
            else if (message.attachment.type == 'simple_list' || message.attachment.type == 'create_order') {
              html = `<ul class='list-unstyled'>`
              for (let item of message.attachment.data) {
                html += `<li>${item}</li>`
              }
              html += `</ul>`
            }

            // Ako smo generisali HTML, šaljemo ga kao poruku
            if (html) {
              this.messages.push({ type: 'bot', text: html })
            }

            // Slučaj: redirekcija na rezervaciju
            if (message.attachment.type == 'order_toy') {
              this.router.navigateByUrl(`/toy/${(message.attachment.data as ToyModel).toyId}/reservation`)
            }
          }

          // DRUGO: Ispisujemo tekstualni deo poruke (npr. "Here are some toys")
          if (message.text) {
            this.messages.push({ type: 'bot', text: message.text })
          }
        }
      })
      .catch(() => {
        this.removeBotPlaceholder()
        this.waitingForResponse = false
        this.messages.push({
          type: 'error',
          text: 'Sorry, something went wrong! Try again later.'
        })
      })
  }

  removeBotPlaceholder() {
    this.messages = this.messages.filter(m => m.text !== this.botThinkingPlaceholder)
  }

  getUserName() {
    const user = UserService.getActiveUser()
    return user ? `${user.firstname} ${user.lastname}` : 'Guest'
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
      "Logout Now",
      "Don't Logout"
    )
  }
}