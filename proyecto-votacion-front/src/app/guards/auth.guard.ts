import { CanMatchFn } from '@angular/router';
import { inject, } from '@angular/core';
import { UserService } from '../services/user.service';
export const authGuard: CanMatchFn = (route, segments) => {

  const userService = inject(UserService);

  console.log("!userService.getAdmin()");
  console.log(userService.getAdmin());

  console.log(Object.keys(userService.getAdmin()).length === 0);


  console.log(!userService.getAdmin);
  console.log("userService.getUsuario()");
  console.log(!userService.getUsuario());

  if (Object.keys(userService.getAdmin()).length === 0 && Object.keys(userService.getUsuario()).length === 0) {
    console.log('entro');

    return Promise.resolve(false);
  }



  return Promise.resolve(true);
};
