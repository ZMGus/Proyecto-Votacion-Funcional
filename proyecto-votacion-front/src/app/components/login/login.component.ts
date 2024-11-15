import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { ApiService } from '../../services/api.service';
import { HttpResponse } from '@angular/common/http';
import Swal from 'sweetalert2';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  constructor(private apiService: ApiService,
    private userService: UserService, private router: Router) {

    }

  form: FormGroup = new FormGroup({});


  ngOnInit(): void {
    this.initForm();

  }


  initForm() {
    this.form = new FormGroup({
      rut: new FormControl(''),
      codigo_acceso: new FormControl(''),
    });
  }

  submit() {
    if (this.form.valid) {
      const rut = this.form.value.rut.split('-')[0];
      const dv = this.form.value.rut.split('-')[1];
      const accessCode = this.form.value.codigo_acceso;
  
      this.apiService.login(rut, dv, accessCode).subscribe({
        next: (response) => {
          if (response.statusCode === 200) {

            // Guarda el usuario en el servicio
            this.userService.setUsuario(response.votante);
  
            // Redirige a la vista de ferias
            this.router.navigate(['/ferias'], {
              queryParams: { activa: true }
            });
          }
        },
        error: (error) => {
          console.error('Error en el login:', error);
          Swal.fire({
            title: 'Error al iniciar sesión',
            text: 'Verifica tus credenciales e intenta nuevamente',
            icon: 'error'
          });
        }
      });
    }
  }
  
  goToAdminLogin() {
    this.router.navigate(['/admin/login']);
  }


}
