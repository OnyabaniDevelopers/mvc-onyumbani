import { NgModule } from '@angular/core';

import { PasswordInputComponent } from './smart.passwordinput';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [PasswordInputComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [PasswordInputComponent]
})

export class PasswordInputModule { }
