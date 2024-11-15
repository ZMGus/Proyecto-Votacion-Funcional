import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../../services/admin.service';
import { MatDialogRef } from '@angular/material/dialog';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-dialog-consultar-codigo',
  templateUrl: './dialog-consultar-codigo.component.html',
  styleUrls: ['./dialog-consultar-codigo.component.scss']
})
export class DialogConsultarCodigoComponent {
  consultaForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    private dialogRef: MatDialogRef<DialogConsultarCodigoComponent>
  ) {
    this.consultaForm = this.fb.group({
      rut: ['', Validators.required],
      dv: ['', Validators.required]
    });
  }

  consultarCodigo() {
    if (this.consultaForm.invalid) {
      Swal.fire('Error', 'Por favor ingrese RUT y DV válidos', 'error');
      return;
    }
    const { rut, dv } = this.consultaForm.value;

    this.adminService.obtenerCodigoAcceso(rut, dv).subscribe({
      next: (response) => {
        Swal.fire('Código de Acceso', `El código es: ${response.codigo_acceso}`, 'info');
        this.dialogRef.close();
      },
      error: () => {
        Swal.fire('Error', 'No se encontró el votante', 'error');
      }
    });
  }
  closeDialog() {
    this.dialogRef.close();
  }
}
