import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../../services/api.service';
import Swal from 'sweetalert2';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-login-admin',
  templateUrl: './login-admin.component.html',
  styleUrls: ['./login-admin.component.scss']
})
export class LoginAdminComponent implements OnInit {
  form: FormGroup = new FormGroup({});

  constructor(private apiService: ApiService, private router: Router, private userService : UserService) {}

  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
    this.form = new FormGroup({
      email: new FormControl(''),
      password: new FormControl('')
    });
  }

  onSubmit() {
    if (this.form.valid) {
        const { email, password } = this.form.value;
        this.apiService.adminLogin(email, password).subscribe({
            next: (response: any) => {
                if (response.statusCode === 200) {
                  console.log(response);
                  this.userService.setAdmin(response.votante);
                  console.log(this.userService.getAdmin());


                    Swal.fire({
                        title: response.message,
                        icon: 'success'
                    });
                    this.router.navigate(['/admin/analitica']);
                }
            },
            error: (error: any) => {
                console.error(error);
                Swal.fire({
                    title: 'Error',
                    text: error.error.detail || 'Error de autenticación',
                    icon: 'error'
                });
            }
        });
    }
}
}

