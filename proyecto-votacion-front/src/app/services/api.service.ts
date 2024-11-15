import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

interface LoginResponse {
  statusCode: number;
  votante: {
    id_votante: number;
    nombre: string;
    email: string;
  };
}


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private url = 'http://votacion.feriadesoftware.cl:8000';

  constructor(private http: HttpClient) { }

  login(rut: number, dv: string, accessCode: string): Observable<LoginResponse> {
    const urlApi = `${this.url}/votante/ingreso`;
    return this.http.post<LoginResponse>(urlApi, { rut, dv, codigo_acceso: accessCode }).pipe(
      tap((response: LoginResponse) => {
        const votanteId = response?.votante.id_votante;
        if (votanteId) {
          console.log('Guardando votanteId en localStorage:', votanteId);
          localStorage.setItem('votanteId', votanteId.toString());
        } else {
          console.warn('No se pudo obtener el votanteId del response');
        }
      })
    );
  }

  

  obtenerFeriaActual(): Observable<any> {
    return this.http.get(`${this.url}/feria`);
}

  obtenerCategoriasPorFeria(): Observable<any> {
    return this.http.get(`${this.url}/ferias/categorias`);
  }

  obtenerProyectosPorCategoria(idcategoria: number): Observable<any> {
    return this.http.get(`${this.url}/categorias/${idcategoria}/proyectos`);
  }

  votarProyecto(proyecto_id: number, votante_id: number): Observable<any> {
    let data = { votante_id: votante_id, proyecto_id: proyecto_id };

    return this.http.post(`${this.url}/votar`, data);
  }

  adminLogin(email: string, password: string): Observable<any> {
    let urlApi = `${this.url}/admin/login`;
    return this.http.post(`${urlApi}`, { email, password });
}

buscarProyecto(keyword: string): Observable<any[]> {
  return this.http.get<any[]>(`${this.url}/proyectos/search?nombre=${keyword}`);
}

// Verificar si el usuario ya ha votado en una categoría específica
verificarVoto(votanteId: number, categoriaId: number): Observable<{ ha_votado: boolean }> {
  return this.http.get<{ ha_votado: boolean }>(`${this.url}/votos/verificar/${votanteId}/${categoriaId}`);
}

verificarVotosCompletados(votanteId: number): Observable<{ votosRestantes: number }> {
  return this.http.get<{ votosRestantes: number }>(`${this.url}/votos/verificar-completados/${votanteId}`);
}

}
