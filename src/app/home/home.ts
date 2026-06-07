import { Component, signal } from '@angular/core';
import { ToyService } from '../../services/toy.service';
import { ToyModel } from '../../models/toy.model';
import { RouterLink } from '@angular/router';
import { FormsModule } from "@angular/forms";

@Component({
  selector: 'app-home',
  imports: [RouterLink, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {

  protected toys = signal<ToyModel[]>([])
  protected allToys: ToyModel[] = []
  protected search = ''

  constructor() {
    this.loadToys()
  }

  protected async loadToys() {

    // prvi put učitava sve igračke
    if(this.allToys.length == 0){
      const rsp = await ToyService.getToys()
      this.allToys = rsp.data
    }

    // filtriranje
    const filtered = this.allToys.filter(toy =>
      toy.name.toLowerCase().includes(this.search.toLowerCase())
    )

    this.toys.set(filtered)
  }
}