import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-dashboard-ferias',
  templateUrl: './dashboard-ferias.component.html',
  styleUrls: ['./dashboard-ferias.component.scss']
})
export class DashboardFeriasComponent implements OnInit {
  feria = signal<any>({});
  categories = signal<any[]>([]);
  votosUsuario: { [key: number]: boolean } = {};

  constructor(private apiService: ApiService, private router: Router,private userService: UserService) {}


  ngOnInit(): void {
    this.obtenerFeriaActual();
    this.apiService.verificarVotosCompletados(this.userService.getUsuario().id_votante).subscribe({
      next: (response) => {
        if (response.votosRestantes === 0) {
          // Usuario ha completado sus votos
          this.userService.setVotosCompletados(true);
          Swal.fire({
            title: 'Ya has votado en todas las categorías',
            text: 'Muchas gracias por participar en la feria.',
            icon: 'info',
            confirmButtonText: 'Volver al inicio de sesión'
          }).then(() => {
            this.router.navigate(['/login']);
          });
        } else {
          // Aún le quedan votos
          this.obtenerFeriaActual();
          this.verificarVotos();
        }
      },
      error: (error) => {
        console.error('Error al verificar votos completados:', error);
      }
    });
  }


  obtenerFeriaActual() {
    this.apiService.obtenerFeriaActual().subscribe({
      next: (response) => {
        // Asignar la respuesta directamente al objeto
        this.feria.set(response);
      },
      error: (error) => {
        console.error(error);
        Swal.fire('Error', 'No se pudieron cargar las ferias', 'error');
      }
    });
  }

  verificarVotos() {
    const votanteId = localStorage.getItem('votanteId');
    if (votanteId) {
      console.log('Verificando votos para votanteId:', votanteId);
      this.categories().forEach((categoria) => {
        this.apiService.verificarVoto(parseInt(votanteId), categoria.id).subscribe({
          next: (response) => {
            console.log(`Respuesta del endpoint para categoría ${categoria.id}:`, response);
            this.votosUsuario[categoria.id] = response.ha_votado;
          },
          error: (error) => {
            console.error(`Error al verificar voto para categoría ${categoria.id}:`, error);
          }
        });
      });
    } else {
      console.warn('No se encontró el votanteId en localStorage o es inválido');
    }
  }

  verCategorias(id: any) {
    this.router.navigate(['/categorias'], { queryParams: { feria: id } });
  }
}

