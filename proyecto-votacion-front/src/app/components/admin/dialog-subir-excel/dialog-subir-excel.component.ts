import { Component } from '@angular/core';
import { AdminService } from '../../../services/admin.service';

@Component({
  selector: 'app-dialog-subir-excel',
  templateUrl: './dialog-subir-excel.component.html',
  styleUrl: './dialog-subir-excel.component.scss'
})
export class DialogSubirExcelComponent {
  constructor(private adminService: AdminService) { }
  selectedFile: any = null;

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0] ?? null;


  }

  onUpload(): void {
    if (this.selectedFile) {
      this.adminService.uploadExcel(this.selectedFile).subscribe({
        next: (response: any) => {
          console.log(response);
        },
        error: (error: any) => {
          console.error(error);
        }
      });
    }
  }
}
