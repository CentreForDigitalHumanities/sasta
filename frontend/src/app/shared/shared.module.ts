import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccordionModule } from 'primeng/accordion';
import { CheckboxModule } from 'primeng/checkbox';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { FieldsetModule } from 'primeng/fieldset';
import { FileUploadModule } from 'primeng/fileupload';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { ToastModule } from 'primeng/toast';
import { TooltipModule } from 'primeng/tooltip';
import { PanelModule } from 'primeng/panel';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { StepsModule } from 'primeng/steps';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule } from '@angular/forms';
import { RenderStringArrayPipe } from './pipes/render-string-array.pipe';

const primeNGModules = [
    // PrimeNG
    AccordionModule,
    CheckboxModule,
    ConfirmDialogModule,
    DialogModule,
    DropdownModule,
    FieldsetModule,
    FileUploadModule,
    MessageModule,
    MessagesModule,
    ToastModule,
    TooltipModule,
    PanelModule,
    ProgressSpinnerModule,
    StepsModule,
];

@NgModule({
    declarations: [RenderStringArrayPipe],
    imports: [CommonModule, FontAwesomeModule, FormsModule, ...primeNGModules],
    exports: [
        ...primeNGModules,
        FontAwesomeModule,
        FormsModule,
        RenderStringArrayPipe,
    ],
})
export class SharedModule {}
