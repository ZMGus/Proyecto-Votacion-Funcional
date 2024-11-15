import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import Swal from 'sweetalert2';
import { ApiService } from '../../services/api.service';
import { UserService } from '../../services/user.service';
import { Location } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard-proyectos',
  templateUrl: './dashboard-proyectos.component.html',
  styleUrls: ['./dashboard-proyectos.component.scss']
})
export class DashboardProyectosComponent implements OnInit {
  searchQuery: string = '';
  idCategoria = signal<number>(0);
  selectedProyectoId: number | null = null;
  proyectos = signal<any[]>([]);
  proyectosFiltrados: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private apiServe: ApiService,
    private userService: UserService,
    private location: Location,
    private sanitizer: DomSanitizer,
    private router: Router 
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const categoria = params['categoria'];
      this.idCategoria.set(categoria);
      this.obtenerProyectos(this.idCategoria());
    });
  }

  obtenerProyectos(idCategoria: number) {
    this.apiServe.obtenerProyectosPorCategoria(idCategoria).subscribe({
      next: (response) => {
        this.proyectos.set(response);
        this.proyectosFiltrados = response; // Inicialmente mostrar todos
      },
      error: (error) => {
        console.error(error);
        Swal.fire('Error', 'No se pudieron cargar los proyectos', 'error');
      }
    });
  }

  buscarProyecto() {
    const query = this.searchQuery.trim().toLowerCase();
    if (query === '') {
      this.proyectosFiltrados = this.proyectos(); // Mostrar todos si no hay búsqueda
    } else {
      this.proyectosFiltrados = this.proyectos().filter(proyecto => 
        proyecto.nombre_proyecto.toLowerCase().includes(query)
      );
    }
  }
  
    confirmarVotacion() {
      if (!this.selectedProyectoId) {
        Swal.fire('Advertencia', 'Por favor, selecciona un proyecto para votar', 'warning');
        return;
      }
    
      this.apiServe.votarProyecto(this.selectedProyectoId, this.userService.getUsuario().id_votante).subscribe({
        next: () => {
          Swal.fire({
            title: 'Voto registrado',
            text: 'Tu voto ha sido registrado exitosamente',
            icon: 'success',
            confirmButtonText: 'Volver a categorías'
          }).then(() => {
            // Redirigir utilizando el enrutador de Angular
            this.router.navigate(['/categorias']);
          });
        },
        error: (error) => {
          if (error.status === 400 && error.error.detail === "El votante ya tiene un voto en esta categoría") {
            Swal.fire('Ya has votado', 'Ya tienes un voto registrado en esta categoría', 'warning');
          } else {
            Swal.fire('Hubo un problema', 'Hubo un problema al registrar tu voto', 'error');
          }
        }
      });
    }


  // Función para sanitizar SVG
  sanitazeSVG(svg: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(svg);
  }

  // Codificar URL para las imágenes
  encodeURIImg(element: any) {
    return encodeURI(element);
  }
}
