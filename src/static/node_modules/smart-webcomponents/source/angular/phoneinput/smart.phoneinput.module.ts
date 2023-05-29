import { NgModule } from '@angular/core';

import { PhoneInputComponent } from './smart.phoneinput';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [PhoneInputComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [PhoneInputComponent]
})

export class PhoneInputModule { }
