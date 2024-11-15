import { HttpClient, HttpHeaders,HttpParams  } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  private url = 'http://votacion.feriadesoftware.cl:8000';

  constructor(private http: HttpClient) { }


  getVotos() {
    return this.http.get(`${this.url}/votos/datos`);
  }

  getVotosCategoria() {
    return this.http.get(`${this.url}/categorias/votos`);
  }

  getVotosProyecto() {
    return this.http.get(`${this.url}/proyectos/votos`);
  }

  uploadExcel(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);


    const headers = new HttpHeaders({
      'enctype': 'multipart/form-data',
    });
    return this.http.post(`${this.url}/admin/upload_excel`, formData, { headers });
  }

  descargarPDF(){
    let url = `${this.url}/admin/resultados/pdf`;
    let options = { responseType: 'blob' as 'json' };
    return this.http.get<any>(url, options);
  }
  
  descargarExcel(): Observable<Blob> {
    const url = `${this.url}/admin/resultados/excel`;
    let options = { responseType: 'blob' as 'json' };
    return this.http.get<any>(url, options);
}
registrarVotante(votanteData: any): Observable<any> {
  return this.http.post(`${this.url}/votante`, votanteData);
}

obtenerCodigoAcceso(rut: string, dv: string): Observable<any> {
  return this.http.get<any>(`${this.url}/votante/codigo?rut=${rut}&dv=${dv}`);
}
}
