import { Component, OnInit, signal } from '@angular/core';
import { AdminService } from '../../../services/admin.service';
import { MatDialog } from '@angular/material/dialog';
import { DialogSubirExcelComponent } from '../dialog-subir-excel/dialog-subir-excel.component';
import Swal from 'sweetalert2';
import { DialogInscripcionVotanteComponent } from '../dialog-inscripcion-votante/dialog-inscripcion-votante.component';
import { DialogConsultarCodigoComponent } from '../dialog-consultar-codigo/dialog-consultar-codigo.component';


@Component({
  selector: 'app-dashboard-analitica',
  templateUrl: './dashboard-analitica.component.html',
  styleUrls: ['./dashboard-analitica.component.scss']
})
export class DashboardAnaliticaComponent implements OnInit {
  constructor(private adminService: AdminService, private dialog: MatDialog) { }
  
  // Usamos signal para manejar el estado de los votos
  votos = signal<any>({});

  ngOnInit(): void {
    this.getVotos();
    this.IntervaloGetVotos();
  }

  // Método para obtener los votos cada 10 segundos
  IntervaloGetVotos(): void {
    setInterval(() => {
      this.getVotos();
    }, 10000);
  }

  // Método para obtener los votos desde el servicio
  getVotos() {
    this.adminService.getVotos().subscribe({
      next: (data: any) => {
        this.votos.set(data);
        this.votos().votos_proyectos.sort((a: any, b: any) => b.votos - a.votos);
      },
      error: (error) => {
        console.error("Error al obtener votos:", error);
      }
    });
  }

  // Método para abrir el diálogo de subir Excel
  openDialogSubirExcel() {
    this.dialog.open(DialogSubirExcelComponent, {
      width: '500px',
      height: '220px'
    });
  }
  openDialogInscripcionVotante(): void {
    const dialogRef = this.dialog.open(DialogInscripcionVotanteComponent, {
      width: '400px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
      }
    });
  }

  openDialogConsultarCodigo(): void {
    this.dialog.open(DialogConsultarCodigoComponent, {
      width: '400px',
      height: '300px'
    });
  }


  // Método para filtrar proyectos por categoría
  filtrarProyectosPorCategoria(categoria: string) {
    if (!this.votos().votos_proyectos) {
      return [];
    }
    return this.votos()
      .votos_proyectos
      .filter((proyecto: any) => proyecto.nombre_categoria === categoria)
      .sort((a: any, b: any) => b.votos - a.votos);
  }

  // Método para descargar PDF
  descargarPDF() {
    this.adminService.descargarPDF().subscribe({
      next: (response: any) => {
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'Resultados.pdf');
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        Swal.fire('Descarga exitosa', 'El archivo PDF se ha descargado correctamente', 'success');
      },
      error: (error: any) => {
        console.error("Error al descargar PDF:", error);
      }
    });
  }

  // Método para descargar Excel
  descargarExcel() {
    this.adminService.descargarExcel().subscribe({
      next: (response: any) => {
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'Resultados.xlsx');
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        Swal.fire('Descarga exitosa', 'El archivo Excel se ha descargado correctamente', 'success');
      },
      error: (error: any) => {
        console.error("Error al descargar Excel:", error);
        Swal.fire('Error', 'No se pudo descargar el archivo Excel', 'error');
      }
    });
  }
}

