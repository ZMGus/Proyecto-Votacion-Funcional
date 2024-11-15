import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { DashboardCategoriasComponent } from './components/dashboard-categorias/dashboard-categorias.component';
import { userResolver } from './resolvers/user.resolver';
import { DashboardProyectosComponent } from './components/dashboard-proyectos/dashboard-proyectos.component';
import { DashboardFeriasComponent } from './components/dashboard-ferias/dashboard-ferias.component';
import { LoginAdminComponent } from './components/admin/login-admin/login-admin.component';
import { DashboardAnaliticaComponent } from './components/admin/dashboard-analitica/dashboard-analitica.component';
import { authGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'admin/login',
    component: LoginAdminComponent
  },
  {
    path: 'admin/analitica',
    component: DashboardAnaliticaComponent,
    canMatch: [authGuard]
  },
  {
    path: 'ferias',
    component: DashboardFeriasComponent,
    resolve: { userResolver },
    canMatch: [authGuard]
  },
  {
    path: 'categorias',
    component: DashboardCategoriasComponent,
    resolve: { userResolver },
    canMatch: [authGuard]
  },
  {
    path: 'proyectos',
    component: DashboardProyectosComponent,
    resolve: { userResolver },
    canMatch: [authGuard]
  },

  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/login',
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
