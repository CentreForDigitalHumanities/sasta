import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccordionModule } from 'primeng/accordion';
import { CheckboxModule } from 'primeng/checkbox';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { DialogModule } from 'primeng/dialog';
import { SelectModule } from 'primeng/select';
import { FieldsetModule } from 'primeng/fieldset';
import { FileUploadModule } from 'primeng/fileupload';
import { MessageModule } from 'primeng/message';
import { TableModule } from 'primeng/table';
import { ToastModule } from 'primeng/toast';
import { TooltipModule } from 'primeng/tooltip';
import { PanelModule } from 'primeng/panel';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { StepsModule } from 'primeng/steps';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule } from '@angular/forms';

const primeNGModules = [
    // PrimeNG
    CheckboxModule,
    ConfirmDialogModule,
    DialogModule,
    SelectModule,
    FieldsetModule,
    FileUploadModule,
    MessageModule,
    TableModule,
    ToastModule,
    TooltipModule,
    PanelModule,
    ProgressSpinnerModule,
    StepsModule,
];

@NgModule({
    declarations: [],
    imports: [CommonModule, FontAwesomeModule, FormsModule, ...primeNGModules],
    exports: [...primeNGModules, FontAwesomeModule, FormsModule],
})
export class SharedModule {}
