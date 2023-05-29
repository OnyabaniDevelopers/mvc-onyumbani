import { NgModule } from '@angular/core';

import { EditorComponent } from './smart.editor';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [EditorComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [EditorComponent]
})

export class EditorModule { }
