import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './upload.component';
import { SharedModule } from '../shared/shared.module';
import { NewCorpusComponent } from './new-corpus/new-corpus.component';

@NgModule({
    declarations: [UploadComponent, NewCorpusComponent],
    imports: [CommonModule, SharedModule],
    exports: [UploadComponent],
})
export class UploadModule {}
