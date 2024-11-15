import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AdminService } from '../../../services/admin.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-dialog-inscripcion-votante',
  templateUrl: './dialog-inscripcion-votante.component.html',
  styleUrls: ['./dialog-inscripcion-votante.component.scss']
})
export class DialogInscripcionVotanteComponent {
  votanteForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    public dialogRef: MatDialogRef<DialogInscripcionVotanteComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.votanteForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      rut: ['', Validators.required],
      dv: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit() {
    if (this.votanteForm.valid) {
      this.adminService.registrarVotante(this.votanteForm.value).subscribe({
        next: (response: any) => {
          this.dialogRef.close();
          Swal.fire('Registro exitoso', `Código Generado: ${response.codigo_acceso}`, 'success');
        },
        error: (error: any) => {
          Swal.fire('Error', 'No se pudo registrar al votante', 'error');
        }
      });
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}

