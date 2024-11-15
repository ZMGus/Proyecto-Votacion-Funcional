import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() title: string = '';
  @Input() backRoute: string | null = null;

  constructor(private router: Router) {}

  navigateBack() {
    if (this.backRoute) {
      console.log("Navegando a:", this.backRoute); 
      this.router.navigate([this.backRoute]);
    }
  }
}
