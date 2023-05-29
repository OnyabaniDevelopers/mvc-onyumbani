import { NgModule } from '@angular/core';

import { QRcodeComponent } from './smart.qrcode';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [QRcodeComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [QRcodeComponent]
})

export class QRcodeModule { }
