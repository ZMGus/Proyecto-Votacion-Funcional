import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router'
import Swal from 'sweetalert2';

@Component({
  selector: 'app-dashboard-categorias',
  templateUrl: './dashboard-categorias.component.html',
  styleUrls: ['./dashboard-categorias.component.scss']
})
export class DashboardCategoriasComponent implements OnInit {
  categories = signal<any[]>([]);
  votosUsuario: { [key: number]: boolean } = {};

  constructor(private api: ApiService, private router: Router,private userService: UserService, ) {}

  ngOnInit(): void {
    this.obtenerCategorias();
    this.api.verificarVotosCompletados(this.userService.getUsuario().id_votante).subscribe({
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
          this.obtenerCategorias();
          this.verificarVotos();
        }
      },
      error: (error) => {
        console.error('Error al verificar votos completados:', error);
      }
    });
  }

  obtenerCategorias() {
    this.api.obtenerCategoriasPorFeria().subscribe({
      next: (response) => {
        const categoriasConImagen = response.map((categoria: any) => ({
          ...categoria,
          imagen: this.encodeURIImg(categoria.imagen)
        }));
        this.categories.set(categoriasConImagen);
        this.verificarVotos();
      },
      error: (error) => {
        console.error('Error al obtener categorías:', error);
      }
    });
  }

  verificarVotos() {
    const votanteId = localStorage.getItem('votanteId');
    if (votanteId) {
      console.log('Verificando votos para votanteId:', votanteId);
      this.categories().forEach((categoria) => {
        this.api.verificarVoto(parseInt(votanteId), categoria.id).subscribe({
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
  
  haVotadoEnCategoria(categoriaId: number): boolean {
    const haVotado = this.votosUsuario[categoriaId] === true;
    console.log(`haVotadoEnCategoria - Categoría ${categoriaId}:`, haVotado);
    return haVotado;
  }
  
  trackByCategoryId(index: number, categoria: any): number {
    return categoria.id;
  }

  verProyectos(categoriaId: number) {
    if (this.haVotadoEnCategoria(categoriaId)) {
      console.log(`Ya has votado en la categoría ${categoriaId}`);
      return;
    }
    this.router.navigate(['/proyectos'], { queryParams: { categoria: categoriaId } });
  }

  encodeURIImg(element: string): string {
    return element ? encodeURI(element) : '';
  }
}


