import { ResolveFn } from '@angular/router';
import { UserService } from '../services/user.service';
import { inject } from '@angular/core';

export const userResolver: ResolveFn<{}> = (route, state) => {
  const userService = inject(UserService);

  return userService.loadUser();
};
