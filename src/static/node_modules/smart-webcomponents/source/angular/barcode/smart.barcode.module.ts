import { NgModule } from '@angular/core';

import { BarcodeComponent } from './smart.barcode';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [BarcodeComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [BarcodeComponent]
})

export class BarcodeModule { }
