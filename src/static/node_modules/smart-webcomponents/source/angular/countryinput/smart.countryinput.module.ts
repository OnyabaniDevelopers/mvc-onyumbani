import { NgModule } from '@angular/core';

import { CountryInputComponent } from './smart.countryinput';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [CountryInputComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [CountryInputComponent]
})

export class CountryInputModule { }
