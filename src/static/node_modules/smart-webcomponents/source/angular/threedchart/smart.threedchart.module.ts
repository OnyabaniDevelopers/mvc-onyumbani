import { NgModule } from '@angular/core';

import { ThreeDChartComponent } from './smart.threedchart';
import { CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';

@NgModule({
    declarations: [ThreeDChartComponent],
	schemas: [CUSTOM_ELEMENTS_SCHEMA],
	exports: [ThreeDChartComponent]
})

export class ThreeDChartModule { }
