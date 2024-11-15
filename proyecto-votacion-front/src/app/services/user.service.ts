import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }

  votante = signal<any>({});
  admin = signal<any>({});

  private userSubject = new BehaviorSubject<any>(null);
  usuarioConectado = this.userSubject.asObservable();

  private adminSubject = new BehaviorSubject<any>(null);
  adminConectado = this.adminSubject.asObservable();

  setUsuario(usuario: any) {
    this.votante.set(usuario);
  }

  getUsuario() {
    return this.votante();
  }

  setAdmin(admin: any) {
    this.admin.set(admin);
  }

  getAdmin() {
    return this.admin();
  }


  loadUser() {
    if (!this.userSubject.value) {
      this.userSubject.next(this.getUsuario());
    }

    return this.usuarioConectado;
  }

  loadAdmin() {
    if (!this.adminSubject.value) {
      this.adminSubject.next(this.getAdmin());
    }

    return this.adminConectado;
  }

  setVotosCompletados(completados: boolean) {
    localStorage.setItem('votosCompletados', completados.toString());
  }

  haCompletadoVotos(): boolean {
    return localStorage.getItem('votosCompletados') === 'true';
  }

  
}
