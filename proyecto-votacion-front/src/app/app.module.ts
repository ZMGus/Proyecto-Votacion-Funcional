import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import { MaterialModule } from './material.module';

import { provideHttpClient } from '@angular/common/http';

import { LoginComponent } from './components/login/login.component';
import { LoginAdminComponent } from './components/admin/login-admin/login-admin.component';
import { DashboardCategoriasComponent } from './components/dashboard-categorias/dashboard-categorias.component';
import { DashboardProyectosComponent } from './components/dashboard-proyectos/dashboard-proyectos.component';
import { DashboardFeriasComponent } from './components/dashboard-ferias/dashboard-ferias.component';
import { DialogSubirExcelComponent } from './components/admin/dialog-subir-excel/dialog-subir-excel.component';
import { DashboardAnaliticaComponent } from './components/admin/dashboard-analitica/dashboard-analitica.component';
import { HeaderComponent } from './shared/header/header.component';
import { DialogInscripcionVotanteComponent } from './components/admin/dialog-inscripcion-votante/dialog-inscripcion-votante.component';
import { DialogConsultarCodigoComponent } from './components/admin/dialog-consultar-codigo/dialog-consultar-codigo.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    LoginAdminComponent,
    DashboardCategoriasComponent,
    DashboardProyectosComponent,
    DashboardFeriasComponent,
    DashboardAnaliticaComponent,
    DialogSubirExcelComponent,
    HeaderComponent,
    DialogInscripcionVotanteComponent,
    DialogConsultarCodigoComponent
 
  ],
  imports: [BrowserModule, AppRoutingModule, BrowserAnimationsModule, FormsModule, ReactiveFormsModule, MaterialModule,],
  providers: [
    provideAnimationsAsync(),
    provideHttpClient()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
